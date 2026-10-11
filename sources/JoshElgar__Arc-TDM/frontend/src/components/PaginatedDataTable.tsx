import { AppSelect } from "./AppSelect";

type PaginatedDataTableProps = {
  columns: string[];
  rows: Record<string, unknown>[];
  page: number;
  pageSize: number;
  hasNext: boolean;
  isLoading?: boolean;
  emptyLabel?: string;
  onRowClick?: (row: Record<string, unknown>) => void;
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
};

const pageSizes = [50, 100, 250, 500];

export function PaginatedDataTable({
  columns,
  rows,
  page,
  pageSize,
  hasNext,
  isLoading,
  emptyLabel = "No rows.",
  onRowClick,
  onPageChange,
  onPageSizeChange
}: PaginatedDataTableProps) {
  return (
    <div className="native-table-shell">
      <div className="native-table-scroll">
        <table className="native-table" style={{ minWidth: Math.max(980, columns.length * 180) }}>
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column}>{formatHeader(column)}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <tr
                className={onRowClick ? "table-click-row" : undefined}
                key={index}
                onClick={onRowClick ? () => onRowClick(row) : undefined}
                onKeyDown={
                  onRowClick
                    ? (event) => {
                        if (event.key === "Enter" || event.key === " ") {
                          event.preventDefault();
                          onRowClick(row);
                        }
                      }
                    : undefined
                }
                tabIndex={onRowClick ? 0 : undefined}
              >
                {columns.map((column) => {
                  const value = formatCell(row[column]);
                  return (
                    <td key={column} title={value}>
                      <span className="native-table-cell-scroll">{value}</span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
        {!columns.length || (!rows.length && !isLoading) ? (
          <div className="native-table-empty">{emptyLabel}</div>
        ) : null}
      </div>
      <div className="table-pager">
        <button type="button" disabled={page <= 0 || isLoading} onClick={() => onPageChange(page - 1)}>
          Previous
        </button>
        <span>Page {page + 1}</span>
        <button type="button" disabled={!hasNext || isLoading} onClick={() => onPageChange(page + 1)}>
          Next
        </button>
        <div className="table-pager-select">
          <span>Rows</span>
          <AppSelect
            ariaLabel="Rows per page"
            value={String(pageSize)}
            onValueChange={(nextPageSize) => onPageSizeChange(Number(nextPageSize))}
            options={pageSizes.map((size) => ({ label: String(size), value: String(size) }))}
          />
        </div>
      </div>
    </div>
  );
}

function formatHeader(value: string) {
  const label = value.replace(/[_-]+/g, " ").trim();
  if (!label) return "";
  return label.charAt(0).toUpperCase() + label.slice(1);
}

function formatCell(value: unknown) {
  if (value === null || value === undefined) return "";
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return JSON.stringify(value);
}
