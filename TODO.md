# TODO


## My Stuff

In the following I will put to do things/ plans that I want to implement 
either in the near future or as soon as possible

--- 
***TODO***
* Put conditions functions into the entk workflow
    - for specfem, check whether `output_solver.txt` has `End of simulation` 
    at the end
    - for conversion, check existence and time stamp of `.h5` files
    - for processing check existence and time stamp of processed files
    - ...
* Similar for the iterative inversion!

---
***DONE***

Here stuff that is done...


    
## Wenjie's stuff


---
***DONE:***

* Create Automatic Specfem CMTSOLUTION writer
* Create DataRequest Class
* check off warnings in spaceweight and pycmt3d -- DONE(ish) can actually not do anything about it.
* Fix below functions so that they can be implemented in a workflow
* Create automatic workflow to process the data (make equal!) and the window the data using pyflex
* Use inversion algorithm.
* Add Spaceweight, to PyPi and 

---
1. Adios and ASDF
  ASDF is all for seismic data
  Adios is only for model file
  
  SAC or MSEED to ASDF converter:
    https://github.com/computational-seismology/pypaw/blob/master/pypaw/convert.py
    
  Function for data process:
    https://github.com/computational-seismology/pytomo3d/blob/master/pytomo3d/signal/process.py#L161
    
  Window Selection:
    https://github.com/computational-seismology/pytomo3d/blob/master/pytomo3d/window/window.py#L114
    
    FLEXWIN Manual:
      https://geodynamics.org/cig/software/flexwin/flexwin-manual.pdf
      Maggi's FLEXWIN paper
      
    My parameter settings later...
   
  Correct repo for the code:
    https://github.com/computational-seismology/pytomo3d/blob/master/INSTALL.md
    
  Pycmt3d:
    https://github.com/wjlei1990/pycmt3d/blob/master/src/pycmt3d/tests/test_cmt3d.py
    
    doc:
      http://wjlei1990.github.io/pycmt3d/   
  
2. SAC, MSEED
  StationXML: response
  
3. CMT
  obspy.read_events(fn, format="CMTSOLUTION")
  
  
4. specfem3d_globe
  a) You can try to run global models, like prem and s362ani.
