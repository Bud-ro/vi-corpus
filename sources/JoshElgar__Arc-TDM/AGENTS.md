# Project Instructions

Prefer KISS. Keep the architecture simple, visible, and easy to reason about.

Always aim for the simplest possible code and the simplest possible state model. Code should be explicit and mechanically traceable. Messy state is the silent killer of development speed: avoid spaghetti state, implicit or untraceable states, and designs that multiply the number of possible states without a clear payoff.

Prefer the fewest reasonable:
- components
- abstraction layers
- first-class objects
- subtypes
- lines of code

Favor shared helper functions that explicitly derive behavior at runtime over complex or implicit contracts, subtypes, or type hierarchies.

Avoid subtypes unless they remove more complexity than they add. Only add structure when the simpler version is clearly insufficient.

Josh does not care about backwards compatibility in this project unless he explicitly says otherwise. Favor the clean current model over migrations, compatibility shims, or preserving old demo data.

Workspace git is the version backbone. Workflows should run from committed workspace state, runs should store the workflow commit they used, and widgets/reports should point to durable run outputs rather than copying those outputs.

Feature verification should favor simple unit tests. Avoid browser sanity checks or heavier verification unless Josh explicitly asks for them.

UI direction: use Replicate-style minimalism as the main reference point. Prefer sparse, table-first operational screens; strong information hierarchy; thin dividers; restrained borders; compact controls; clear status icons; and simple list/table layouts over decorative cards, heavy chrome, or marketing-style dashboards. Dark mode should stay crisp and high-contrast, with distinctive semantic colors only where they help scanning.

See `DESIGN.md` for the durable Arc styling, layout, data UI, dashboard, workflow, reports, chat, icon, status, and time-formatting direction.
