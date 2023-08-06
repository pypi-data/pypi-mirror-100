# distributions_gj

This is a Python library for working with statistical distributions:


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install distributions_gj.

```bash
pip install distributions_gj
```

## Usage

```python
import distributions_gj

gaussian_one = distributions_gj.Gaussian(mu = 25, sigma = 2)
gaussian_two = distributions_gj.Gaussian(mu = 10, sigma = 4)

gaussian_three = gaussian_one + gaussian_two

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
