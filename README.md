# CarpalTunnelExercises
## Overview
This is a project made as part of the Computer Science in Medicine course at the AGH University of Science and Technology. The aim of the project was to create an app that would allow the user to set an exercise schedule and would then notify the user and verify the completion of the exercises using hand tracking technology.

## Medical basis
We based the exercises used in this app on ones presented in the [doc](https://orthoinfo.aaos.org/globalassets/pdfs/a00789_therapeutic-exercise-program-for-carpal-tunnel_final.pdf?fbclid=IwAR0VP55rjsGtpE0BtL1mOCRiHfpznRW2n96hAvBN_Z74PQKfQm0UMeVb9IY) published by The American Academy of Orthopaedic Surgeons. Please read it before using the app.

## Prerequirements
 - `python` version `3.8` or higher
 - `pip` version `21` or higher
 - Recommended os: `Ubuntu 20.04`

## Installation
 - Clone this repo: `git clone <this repo's address>`.
 - `cd` into the main directory: `CarpalTunnelExercises`
 - Install the dependencies: `pip3 install -r requirements.txt`
 
 ## Setup
 In the current iteration of the app to set your preffered schedule you need to edit the `schedule.json` file. The format of this file is as follows
 
 ```
 {
  "<first exercise code>": {
 
    "reps": <the preffered number of repetition for each hand>,
    "schedule": [
      {
        "hour": <the hour of the first scheduled exercise, for example: 15 if you want to exercise at 15:05>,
        "minute": <the minute of the first scheduled exercise, for example: 5 if you want to exercise at 15:05>
      },
      {
      "hour": <the hour of the second scheduled exercise>
      "minute": <the minute of the second scheduled exercise>
      }
      ...
    ]
  },
    "<second exercise code>": {<analogous to the first>},
    ...
 }
 ```
 
 The supported exercise codes are: `1`, `2`, `3`, `4a`, `4b`. They reference the numbers assigned to the exercises [here](https://orthoinfo.aaos.org/globalassets/pdfs/a00789_therapeutic-exercise-program-for-carpal-tunnel_final.pdf?fbclid=IwAR0VP55rjsGtpE0BtL1mOCRiHfpznRW2n96hAvBN_Z74PQKfQm0UMeVb9IY).

## Running
Run the app with `python3 -m src.scheduling.scheduler`.
