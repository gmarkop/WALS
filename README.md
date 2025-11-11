# The World Atlas of Language Structures Online (WALS)

[![CLDF validation](https://github.com/cldf-datasets/wals/workflows/CLDF-validation/badge.svg)](https://github.com/cldf-datasets/wals/actions?query=workflow%3ACLDF-validation)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Overview

The World Atlas of Language Structures (WALS) is a comprehensive database of structural (phonological, grammatical, lexical) properties of languages gathered from descriptive materials. This repository contains the **CLDF (Cross-Linguistic Data Format)** version of WALS, making the data accessible in a standardized, machine-readable format.

WALS was created by **Matthew S. Dryer** and **Martin Haspelmath** and is available online at [https://wals.info](https://wals.info).

### Key Features

- **2,500+ languages** from diverse language families worldwide
- **192 typological features** covering phonology, morphology, syntax, and lexicon
- **Geographic and genealogical information** for each language
- **Linguistic examples** with interlinear glosses
- **Extensive bibliographic references** linked to data points
- **Genealogical language classification** with family trees

## What's in This Repository

This repository contains:

- **Python conversion script** (`cldfbench_wals.py`) - Converts raw WALS data into CLDF format
- **CLDF dataset** - Structured linguistic data in standardized format
- **Metadata files** - Dataset description and citation information
- **Change logs** - Documentation of updates and corrections since 2008

### Data Structure

The CLDF dataset includes the following main components:

| Table | Description |
|-------|-------------|
| **LanguageTable** | Languages and language groups with geographic coordinates, ISO codes, Glottocodes |
| **ParameterTable** | Typological features (e.g., "Order of Subject, Object and Verb") |
| **CodeTable** | Possible values for each feature (e.g., "SOV", "SVO", "VSO") |
| **ValueTable** | Language-feature data points with references |
| **ContributionTable** | Chapters describing features and methodologies |
| **ExampleTable** | Linguistic examples with interlinear glosses |
| **TreeTable** | Genealogical classification trees |

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/cldf-datasets/wals.git
cd wals

# Install dependencies
pip install -e .
```

### Dependencies

This package requires:

- `cldfbench>=1.6.0` - Framework for CLDF dataset management
- `pycldf>=1.19.0` - Python library for reading/writing CLDF
- `clldutils>=3.7.0` - Utilities for cross-linguistic data
- `pybtex>=0.24.0` - BibTeX parser
- `beautifulsoup4>=4.9.3` - HTML parsing
- `python-nexus` - NEXUS format support for phylogenetic trees
- `newick` - Newick tree format support
- `csvw>=1.10.1` - CSV on the Web metadata

## Usage

### Accessing the CLDF Dataset

The CLDF dataset is located in the `cldf/` directory after running the conversion:

```python
from pycldf import Dataset

# Load the WALS CLDF dataset
ds = Dataset.from_metadata('cldf/StructureDataset-metadata.json')

# Iterate over languages
for language in ds['LanguageTable']:
    print(f"{language['Name']} ({language['ID']})")

# Access typological features
for parameter in ds['ParameterTable']:
    print(f"{parameter['ID']}: {parameter['Name']}")

# Query values for a specific language
for value in ds['ValueTable']:
    if value['Language_ID'] == 'eng':
        print(f"Feature {value['Parameter_ID']}: {value['Value']}")
```

### Using with cldfbench

```bash
# Download raw data (if needed)
cldfbench wals.download

# Create CLDF dataset
cldfbench wals.makecldf

# Run tests
pytest test.py
```

## Data Coverage

### Geographic Distribution

WALS covers languages from all major geographic areas:

- Africa
- Eurasia
- Southeast Asia and Oceania
- Australia and New Guinea
- North America
- South America

### Typological Features

Features are organized into 11 main areas:

1. **Phonology** (19 features)
2. **Morphology** (28 features)
3. **Nominal Categories** (30 features)
4. **Nominal Syntax** (10 features)
5. **Verbal Categories** (20 features)
6. **Word Order** (50 features)
7. **Simple Clauses** (10 features)
8. **Complex Sentences** (7 features)
9. **Lexicon** (7 features)
10. **Sign Languages** (3 features)
11. **Other** (8 features)

### Language Samples

WALS includes two carefully designed language samples:

- **100-language sample** - Balanced for genealogical diversity
- **200-language sample** - Extended balanced sample

These samples are designed to minimize genealogical and areal bias in statistical analyses.

## Data Quality and Updates

### Version History

- **v2020.4** (2024-10-18) - Fixed language metadata errata, updated Glottocodes to Glottolog 5.0
- **v2020.3** (2022-12-01) - Added genealogical trees, proper ContributionTable with citations
- **v2020.2** (2022-07-07) - Language metadata updates
- **v2020.1** (2021-04-13) - Full CLDF implementation with all web data
- **v2020** (2020-03-27) - Minor corrections
- **v2014** - Classification updates, value corrections
- **v2013** - Datapoint corrections
- **v2011** - New chapters (143, 144), genealogical updates
- **v2008** - Initial online version with errata corrections

See [CHANGES.md](CHANGES.md) for detailed change history.

### Quality Control

- All values are linked to bibliographic sources
- Glottocodes validated against Glottolog database
- Regular updates to correct errors and incorporate new research
- Community feedback and error reporting via GitHub issues

## Citation

### Primary Citation

If you use this dataset, please cite the original source:

> Dryer, Matthew S. & Haspelmath, Martin (eds.) 2013. *The World Atlas of Language Structures Online*. Leipzig: Max Planck Institute for Evolutionary Anthropology. (Available online at https://wals.info)

### CLDF Dataset Citation

Also cite the specific version of the CLDF dataset you used:

> Dryer, Matthew S. & Haspelmath, Martin (eds.) 2024. *The World Atlas of Language Structures Online* (CLDF dataset version [VERSION]). Zenodo. DOI: [See released versions](https://github.com/cldf-datasets/wals/releases/)

### Chapter Citations

When citing specific chapters/features, include the chapter author(s):

> [Author(s)]. 2013. [Feature Name]. In: Dryer, Matthew S. & Haspelmath, Martin (eds.) *The World Atlas of Language Structures Online*. Leipzig: Max Planck Institute for Evolutionary Anthropology. (Available online at https://wals.info/chapter/[chapter_id])

## License

This dataset is licensed under a **Creative Commons Attribution 4.0 International License (CC-BY-4.0)**.

You are free to:
- **Share** - copy and redistribute the material in any medium or format
- **Adapt** - remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution** - You must give appropriate credit, provide a link to the license, and indicate if changes were made

See [LICENSE](LICENSE) for full license text.

## Contributing

### Reporting Errors

If you find errors in the data, please:

1. Check if the error has already been reported in [Issues](https://github.com/cldf-datasets/wals/issues)
2. If not, open a new issue with:
   - Language/feature affected
   - Description of the error
   - Source documentation (if available)
   - Suggested correction

### Code Contributions

Contributions to the conversion scripts are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Add tests if applicable
5. Commit with clear messages
6. Push and create a Pull Request

## Development

### Running Tests

```bash
# Install test dependencies
pip install -e .[test]

# Run CLDF validation tests
pytest test.py
```

### Converting Raw Data

The `cldfbench_wals.py` script handles the conversion from raw WALS database exports to CLDF format:

```python
# Main conversion function
cldfbench wals.makecldf --glottolog /path/to/glottolog
```

The script:
1. Reads raw CSV files from the `raw/` directory
2. Processes language metadata and genealogical classifications
3. Converts typological features and values
4. Links bibliographic references
5. Generates CLDF-compliant CSV tables and JSON metadata

## Technical Details

### CLDF Conformance

This dataset conforms to the **CLDF StructureDataset** specification, which is designed for typological/structural linguistic data. It includes:

- Standard CLDF components (Languages, Parameters, Codes, Values)
- Custom tables (Contributors, Areas, Countries, Language Names)
- Foreign key relationships between tables
- Bibliographic sources in BibTeX format
- Media files (chapter descriptions, genealogical trees)

### Genealogical Classification

Languages are organized in a four-level hierarchy:

1. **Family** (e.g., Indo-European, Sino-Tibetan)
2. **Subfamily** (e.g., Germanic, Romance)
3. **Genus** (e.g., West Germanic, Ibero-Romance)
4. **Language** (individual languages)

This classification is encoded in the TreeTable as NEXUS format phylogenetic trees.

### Identifier Integration

WALS languages are linked to external identifier systems:

- **ISO 639-3** codes (when available)
- **Glottocodes** from [Glottolog](https://glottolog.org)
- **WALS codes** (unique 3-letter identifiers)

## Resources

- **WALS Online**: https://wals.info
- **CLDF Specification**: https://cldf.clld.org
- **Glottolog**: https://glottolog.org
- **GitHub Repository**: https://github.com/cldf-datasets/wals
- **Issue Tracker**: https://github.com/cldf-datasets/wals/issues

## Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for a list of contributors to this CLDF dataset.

The original WALS database was created by:

- **Matthew S. Dryer** (Editor)
- **Martin Haspelmath** (Editor)
- **144 chapter authors** (see individual chapters for authorship)
- **Robert Forkel** (Data Manager for CLDF conversion)

## Acknowledgments

WALS was supported by:

- Max Planck Institute for Evolutionary Anthropology (Leipzig)
- Max Planck Digital Library
- Department of Linguistics, University at Buffalo

The CLDF conversion was made possible by the [CLDF](https://cldf.clld.org) and [cldfbench](https://github.com/cldf/cldfbench) frameworks developed by the Cross-Linguistic Data Formats initiative.

## Release Information

For information about creating new releases, see [RELEASING.md](RELEASING.md).

To stay updated with new releases, watch this repository and subscribe to release notifications.
