# robotframework-webscreens

A library to simulate different screen resolutions on current/given url

![PyPI version](https://badge.fury.io/py/robotframework-webscreens.svg)
[![Downloads](https://pepy.tech/badge/robotframework-webscreens)](https://pepy.tech/project/robotframework-webscreens)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

### Installation:

 To install robotframework-webscreens
 ```
 $ pip install robotframework-webscreens==0.1.1
 ```
 Keyword documentation [link](https://robotframework-webscreens.netlify.app/)

### How it works:

 - Adjust browser to resolution (Mobile or Desktop or Table)
 - Navigate/Reload page
 - Capture page screenshot
 - Repate above steps for different resolutions

### Usage:

 ```
*** Settings ***
Library    SeleniumLibrary
Library    WebScreens

*** Test Cases ***
Demo
    Open Browser    http://google.com/    chrome
    Simulate Screen Resolutions    resolution_type=Mobile
    Simulate Screen Resolutions    resolution_type=Desktop    url=https://github.com
    Simulate Screen Resolution    300    720    revert=False
    [Teardown]    Close All Browsers
 ```