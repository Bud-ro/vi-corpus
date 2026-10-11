# LabVIEW Calculator

> [!NOTE]
> This project was created as a learning exercise while I was studying LabVIEW.  
> As such, it may contain mistakes, non-standard implementations, or unnecessarily verbose logic due to my limited familiarity with LabVIEW’s built-in VIs.

## Version
LabVIEW Community 2025 Q3

## Features
- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Square root calculation
- Parentheses **(supports nested expressions)**
- Sign toggle (+/–)
- Reciprocal function (1/x)
- Real-time clock display
- Execution duration timer
- Calculation history (stores recent results)

## Implementation Details
- The calculator evaluates the **entire expression only after pressing the "=" button**, rather than performing step-by-step calculations.
- The expression parser is implemented using the **Shunting Yard Algorithm**, which efficiently handles operator precedence and parentheses **without recursion**.

## Screenshots
<img width="708" height="509" alt="image" src="https://github.com/user-attachments/assets/14f0bdc2-3ef8-42b1-bf23-c3256f73ebc3" />
<img width="364" height="196" alt="image" src="https://github.com/user-attachments/assets/a1230aa4-ecd6-462c-9dab-d59887f17bb7" />

## License
This project is released under the [Apache-2.0 License](LICENSE).
