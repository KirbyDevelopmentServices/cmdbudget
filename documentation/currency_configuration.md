# Currency Configuration

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

## Overview

The currency configuration allows you to specify how cmdbudget handles different currency columns in your CSV files and how to format currency values in reports.

## Configuration Structure

The currency configuration is part of the `import_csv_structure` section in `config.yml`:

```yaml
import_csv_structure:
  # ... other fields ...
  currency_columns:
    CAD: "CAD$"
    USD: "USD$"
  currency_priority: ["CAD", "USD"]
  default_currency: "CAD"
  currency_formatting:
    CAD:
      symbol: "$"
      position: "before"
      decimal_places: 2
    USD:
      symbol: "$"
      position: "before"
      decimal_places: 2
```

## Configuration Options

### currency_columns
A dictionary mapping currency codes to their corresponding CSV column names.

Example:
```yaml
currency_columns:
  CAD: "CAD$"
  USD: "USD$"
  EUR: "EUR€"
```

### currency_priority
A list of currency codes in order of priority. When multiple currency columns have values, the first non-zero amount in the priority order will be used.

Example:
```yaml
currency_priority: ["CAD", "USD", "EUR"]
```

### default_currency
The currency code to use when no specific currency information is available.

Example:
```yaml
default_currency: "CAD"
```

### currency_formatting
Configuration for how to format currency values in reports.

For each currency, you can specify:
- `symbol`: The currency symbol (e.g., "$", "€")
- `position`: Where to place the symbol ("before" or "after")
- `decimal_places`: Number of decimal places to show

Example:
```yaml
currency_formatting:
  CAD:
    symbol: "$"
    position: "before"
    decimal_places: 2
  USD:
    symbol: "$"
    position: "before"
    decimal_places: 2
  EUR:
    symbol: "€"
    position: "after"
    decimal_places: 2
```

## Examples

### Basic Single Currency Setup
```yaml
import_csv_structure:
  currency_columns:
    CAD: "Amount"
  currency_priority: ["CAD"]
  default_currency: "CAD"
  currency_formatting:
    CAD:
      symbol: "$"
      position: "before"
      decimal_places: 2
```

### Multi-Currency Setup
```yaml
import_csv_structure:
  currency_columns:
    CAD: "CAD$"
    USD: "USD$"
    EUR: "EUR€"
  currency_priority: ["CAD", "USD", "EUR"]
  default_currency: "CAD"
  currency_formatting:
    CAD:
      symbol: "$"
      position: "before"
      decimal_places: 2
    USD:
      symbol: "$"
      position: "before"
      decimal_places: 2
    EUR:
      symbol: "€"
      position: "after"
      decimal_places: 2
```

## Best Practices

1. **Column Naming**: Use consistent column names across your CSV files. For example, always use "CAD$" for Canadian dollars.

2. **Priority Order**: Put your most commonly used currency first in the priority list.

3. **Default Currency**: Set your primary currency as the default.

4. **Formatting**: Ensure currency formatting matches your local conventions.

5. **Validation**: The configuration will validate that:
   - All currencies in `currency_priority` exist in `currency_columns`
   - The `default_currency` exists in `currency_columns`
   - All formatting options are valid

## Troubleshooting

### Common Issues

1. **Missing Currency Column**: If a currency column is missing in your CSV, the system will use the default currency.

2. **Invalid Amounts**: Non-numeric values in currency columns will be treated as zero.

3. **Multiple Currencies**: When multiple currency columns have values, the first non-zero amount in the priority order will be used.

### Error Messages

- "Currency 'X' in priority list not found in currency_columns": A currency in your priority list doesn't have a corresponding column mapping.
- "Default currency 'X' not found in currency_columns": Your default currency doesn't have a corresponding column mapping.
- "Invalid currency_columns configuration": The currency_columns section must be a dictionary.
- "Invalid currency_priority configuration": The currency_priority section must be a list.
- "Invalid currency_formatting configuration": The currency_formatting section must be a dictionary. 