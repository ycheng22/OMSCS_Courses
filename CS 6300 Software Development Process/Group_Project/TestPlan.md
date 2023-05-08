# Test Plan

**Author**: Team 046

## 1 Testing Strategy

### 1.1 Overall strategy

We will use Android logcat for development, and then JUnit for final verification.

### 1.2 Test Selection

Both White and Black box testing will be used.
White box testing will be used by adding statements in the code that print information about the User to the logcat. This testing is to help us developers as we build the app.
Black box testing will be used with JUnit tests. This testing will insure that are functionalities are met and provide regression testing for future changes.

### 1.3 Adequacy Criterion

Test cases will cover each screen, with different starting conditions, and different happenings. 

### 1.4 Bug Tracking

Bugs will by caught and reported by users, or caught by regression testing.
There is not plan for enhancements. 

### 1.5 Technology

Android logcat and JUnit will be used.

## 2 Test Cases

| Purpose                     | Steps     | Expected Result | Actual Result | Additional Info |
|-----------------------------|-----------|-----------------|---------------|-----------------|
| 1. Input current job first time     | 1. Click DEBUG-CLEAR DATA <br/> 2. Click CURRENT JOB <br/>  |       The table is blank when the screen shows up firstly    |      As expected         |                 |
| 2. Input current job without saving | 1. Click DEBUG-CLEAR DATA <br/> 2. Click CURRENT JOB <br/> 3. Enter details and click back button | The information of current job is not available in the job list when click COMPARE JOBS button | As expected | | 
| 3. Input current job and save      | 1. Click DEBUG-CLEAR DATA <br/> 2. Click CURRENT JOB <br/> 3. Enter details and click save button |       The information of current job appears in the job list when click COMPARE JOBS button      | As expected |                |
| 4. Input job offers and save | 1. Click JOB OFFERS <br/> 2. Enter details and click save button | The saved job offer will be displayed in  the job list when click COMPARE JOBS button | As expected |                 |
| 5. Enter another job offer | 1. Click JOB OFFERS <br/> 2. Enter details and click save button <br/> 3. Click ENTER ANOTHER OFFER button, enter details, click save button| The saved job offer will be displayed in  the job list when click COMPARE JOBS button | As expected |                 |
|6. Compare with current offer | 1. Click JOB OFFERS <br/> 2. Enter details and click save button <br/> 3. Click COMPARE WITH CURRENT JOB button| The details of current job and job offer will be displayed in  the job list when click COMPARE JOBS button | As expected |                 |
|7. Edit comparison settings and save | 1. Click COMPARISON SETTINGS <br/> 2. Enter detail <br/> 3. Click save button | The updated comparison settings are updated and displayed on the screen | As expected |                 |
|8. Edit comparison settings withou saving | 1. Click COMPARISON SETTINGS <br/> 2. Enter detail <br/> 3. Click back button | The updated comparison settings are not saved when click COMPARISON SETTINGS again| As expected |                 |
|9. Compare jobs | 1. Click COMPARE JOBS button <br/> 2. Choose two jobs from the job list | The two selected jobs will populate the comparison table, if the user click another job, the comparison table will be updated | As expected |                 |
|10. Perform another comparison | 1. Click COMPARE JOBS button <br/> 2. Choose two jobs from the job list <br/> 3. Click COMPARE ANOTHER button and select two jobs from the job list| When click COMPARE ANOTHER button, the comparison table will be cleared, the user can select another two jobs, which will populate the comparison table | As expected |                 |