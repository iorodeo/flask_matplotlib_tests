import flask
import pylab
import os
import os.path
import tempfile
import random

app = flask.Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():

    if flask.request.method == 'POST':   
        if 'plot_button' in flask.request.form:
            x_data_raw = str(flask.request.form['x_data'])
            y_data_raw = str(flask.request.form['y_data'])
            x_data = x_data_raw.split()
            y_data = y_data_raw.split()
            try:
                ok = True
                x_data_float = [float(val) for val in x_data]
                y_data_float = [float(val) for val in y_data]
                x_data_str = '\n'.join(x_data)
                y_data_str = '\n'.join(y_data)
            except ValueError:
                ok = False
                error_msg = 'Error: unable to convert to floating point number'
                x_data_str = x_data_raw
                y_data_str = y_data_raw

            if ok:
                if len(x_data) >= 1 and len(y_data) >= 1:
                    n = min([len(x_data_float), len(y_data_float)])
                    x_data_float = x_data_float[:n]
                    y_data_float = y_data_float[:n]

                    pylab.plot(x_data_float,y_data_float,'o-')
                    pylab.title('Plot Title')
                    pylab.grid('on')
                    pylab.xlabel('x label')
                    pylab.ylabel('y label')
                    filename = os.path.join(os.curdir, 'static', 'plot.png')
                    pylab.savefig(filename)
                    pylab.close()
                    return flask.redirect(flask.url_for('plot_data'))
                else:
                    if len(x_data) < 1:
                        error_msg = 'Error: insufficient x values for plot' 
                    else:
                        error_msg = 'Error: insufficient y values for plot'
        if 'clear_button' in flask.request.form: 
            error_msg = ''
            x_data_str = '' 
            y_data_str = '' 
    else:
        error_msg = ''
        x_data_str = '' 
        y_data_str = '' 

    render_args = {
            'x_data_str': x_data_str,
            'y_data_str': y_data_str,
            'error_msg': error_msg,
            }
    return flask.render_template('index.html',**render_args) 

@app.route('/plot')
def plot_data():
    randint = random.randint(10000,20000)
    return flask.render_template('plot.html',randint=randint) 

if __name__ == '__main__':

    app.debug = True
    app.run()
