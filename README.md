# peoplebox-assignment

## Employee Historical Data Transformation Script

This Python script transforms employee data from a columnar format in a CSV file into a historical, row-based version suitable for database storage. This format facilitates historical analysis of employee compensation, engagement, and performance reviews.


- **Structured Data:** Reorganizes columns of input csv file, placing date-related columns in historical order for better readability.

- **Missing Value Imputation:** Handles missing values in "Last Compensation" and "Compensation" columns by intelligently inheriting values from previous entries (either for the same employee or the preceding record).
  
- **Pay Raise Dates:** Identifies the date of the most recent pay raise for each employee based on changes in their compensation.
  
- **End Date Calculation:** Calculates the end date for each employment record by considering the subsequent record's effective date (if available).



### Prerequisites:

- Python 3.x
- pandas library `pip install pandas`



### Usage:

1. Save the script `script-name.py`
2. Place your `input.csv` file named in the same directory.
3. Run the script



### Explanation of Functions:

- `rearrange_columns:` Sorts columns by identifying date related columns and placing them in historical order.
  
- `inherit_previous_value:` Iterates through the data, carrying forward the most recent non-null values for **Last Compensation** and **Compensation** columns.
  
- `assign_last_pay_raise_date:` Identifies the date of the most recent pay raise based on changes in **Compensation**.
  
- `assign_end_date:` Calculates the **End Date** for each employment record based on the subsequent record's **Effective date**.
