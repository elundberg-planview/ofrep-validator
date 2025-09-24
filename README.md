# OFREP Validator

A command-line tool for validating [OpenFeature Remote Evaluation Protocol (OFREP)](https://openfeature.dev/specification/appendix-b) compliance.

## Usage

```bash
ofrep-validator <base_url> [context...] [--key <flag_key>]
```

### Examples

Test all flags:
```bash
ofrep-validator http://localhost:8080
```

Test with evaluation context:
```bash
ofrep-validator http://localhost:8080 user_id=123 country=US
```

Test a specific flag:
```bash
ofrep-validator http://localhost:8080 --key my-feature-flag
```

Test a specific flag with context:
```bash
ofrep-validator http://localhost:8080 user_id=456 --key my-feature-flag
```

## What it does

The tool sends HTTP POST requests to OFREP endpoints (`/ofrep/v1/evaluate/flags`) to:
- Validate OFREP compliance of feature flag providers
- Test flag evaluation responses
- Pass evaluation context as key-value pairs
- Query specific flags by key or evaluate all flags
