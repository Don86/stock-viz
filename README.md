# stock-viz
Visualization of stock data using Python Flask. 

The trappings of a stock visualization front-end, powered by Python.  The data are extracted using a Yahoo finance API, and displayed using the `Bokeh` and `Flask` libraries. We'll see the pertinent statistics of a selection of stocks - mostly index ETFs and blue chips - that I have personal interest in. New features can be added incrementally as this project increases in scope. 

## Files
`stock-viz.py` - the main Python backend script. 
`fnce_utils.py` - library. Contains a bunch of financial computations.
`templates/stockprofile.html` - HTML file connected to the backend. 
`style.css` - The eponymous css file.
