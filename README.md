# pviz - Availability Impact Analyzer

`pviz` is a command-line tool that helps you understand the real impact of service availability targets (SLAs) by converting availability percentages into actual downtime durations across different time periods.

## Features

- Calculate maximum allowed downtime for different availability targets (99.9%, 99.99%, etc.)
- View downtime impact across different time periods (day, week, month, quarter, year)
- Compare two different availability targets to see the improvement in downtime reduction
- Rich terminal output with formatted tables

## Usage

### Analyze a Single Availability Target

To analyze the impact of a single availability target:

```bash
pviz analyze 99.99
```

You can focus on a specific time period:

```bash
pviz analyze 99.99 --focus month
```

### Compare Two Availability Targets

To compare the downtime impact between two different availability targets:

```bash
pviz compare 99.9 99.99
```

### Available Time Periods

- day
- week
- month
- quarter
- year
