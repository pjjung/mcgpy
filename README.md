## Description
The MCGpy package contains classes and utilities providing tools and methods for analyzing magnetocardiography(MCG) data. It is designed for someone who wants to utilize it for instrumental or medical purposes without knowing detailed algorithms. For this purpose, several key features of the MCGpy are based on the basic concept and ideas of the [GWpy](https://github.com/gwpy/gwpy), developed by Duncan Macleod <duncan.macleod@ligo.org>.

## Status
[![Build Status](https://img.shields.io/badge/build-test%20version-9cf)](https://img.shields.io/badge/build-test%20version-9cf)
[![Build Status](https://img.shields.io/badge/version-0.1-blue)](https://img.shields.io/badge/version-0.1-blue)

[![Build Status](https://img.shields.io/badge/license-%20GPLv3-green)](http://www.gnu.org/licenses/)
[![Build Status](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-brightgreen)](https://minepy.readthedocs.io/en/latest/)


## Installation
- Manual installation
```sh
$ git clone https://github.com/pjjung/mcgpy.git
$ cd mcgpy
$ python setup.py install

```
- or, you can do:
```
# pip installation will be supported
```


## References
Lead field calculation methods were referred to in the following papers:
- M.S Hamalainen, et al., *Interpreting magnetic fields of the brain: minimum orm estimates*,  Med. & Biol. Eng. & Compu., 32, 35-42 (1994)
- J.T. Nenonen, et al., *Minimum-norm estimation in a boundary-element torso model*, Med. & Biol. Eng. & Compu., 32, 42-48 (1994)

## License

The MCGpy is following the GNU General Public License version 3. Under this term, you can redistribute and/or modify it.
See [the GNU free software license](http://www.gnu.org/licenses/) for more details.
