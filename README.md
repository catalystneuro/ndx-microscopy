# ndx-microscopy Extension for NWB

A Neurodata Without Borders (NWB) extension for storing microscopy data and associated metadata in a standardized format. This extension integrates with [ndx-ophys-devices](https://github.com/catalystneuro/ndx-ophys-devices) to provide comprehensive optical component specifications.

## Features

- **Comprehensive Data Types**
  - Microscope and optical component metadata
  - Advanced light path configurations
  - Imaging space definitions
  - Time series data with variable depth support
  - ROI/segmentation storage

- **Multiple Modalities**
  - One-photon microscopy (widefield)
  - Two-photon microscopy
  - Three-photon microscopy
  - Light sheet microscopy

- **Flexible Organization**
  - Support for 2D and 3D imaging
  - Multi-channel data handling
  - Variable depth imaging
  - Coordinate system management

## Installation

```bash
pip install ndx-microscopy
```

For MATLAB users:
```matlab
generateExtension('<directory path>/ndx-microscopy/spec/ndx-microscopy.namespace.yaml');
```

## Basic Usage

```python
from ndx_microscopy import Microscope, ExcitationLightPath, EmissionLightPath
from ndx_ophys_devices import Indicator

# Set up microscope
microscope = Microscope(
    name='2p-scope',
    model='Custom two-photon microscope'
)

# Create indicator
indicator = Indicator(
    name='gcamp6f',
    label='GCaMP6f',
    description='Calcium indicator'
)

# Configure light paths
excitation = ExcitationLightPath(
    name='2p_excitation',
    excitation_wavelength_in_nm=920.0,
    excitation_mode='two-photon'
)

emission = EmissionLightPath(
    name='gcamp_emission',
    emission_wavelength_in_nm=510.0,
    indicator=indicator
)
```

## Documentation

For detailed documentation, including API reference and additional examples, please visit our [documentation site](https://ndx-microscopy.readthedocs.io/).

The documentation includes:
- Getting Started Guide
- User Guide with Best Practices
- Comprehensive Examples
- Complete API Reference
- Data Format Specifications

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License. See [LICENSE.txt](LICENSE.txt) for details.
