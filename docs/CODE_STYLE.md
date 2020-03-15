# Code Style

This documentation provides some code style you have to follow to inorder for your branch be accebted and merged to the master branch. These code style guidlines are in addition to code styles outlined by python community in PEP8. Since every code will be tested against PEP8 using flake8, make sure your code passes these tests in order for your pull request to recognised by the community.

## Characters
standard PEP8 uses 80 character as default, due to the setting.py module we used 110 character as default.

## Naming convention
* when naming class's use python specific naming convention like: 
```python
class AdminDashboard:
```
* when naming methods and functions use **_** for separating words like:
```python
def create_user():
```