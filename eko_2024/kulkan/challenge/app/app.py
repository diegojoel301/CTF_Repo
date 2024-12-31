from flask import Flask, request, render_template
import subprocess
import shlex

app = Flask(__name__)

@app.route('/', methods=['GET'])
def nmap_scan():
    if request.method == 'GET' and request.args:
        host = request.args.get('host')
        command = request.args.get('command')
       
        allowed_commands = ["ping", "dig", "nmap"]

        if command not in allowed_commands:
            return render_template('index.html')

        # If the command is ping, we append the flag -c 4 so it doesn't run indeterminately
        if command == "ping":
            cmd = f"ping -c4 {host}"
        else:
            cmd = f"{command} {host}"
        print(cmd)
        print(shlex.split(cmd))
        try:
            result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=60)
            output = result.stdout if result.returncode == 0 else result.stderr
        except subprocess.TimeoutExpired:
            output = "Scan timed out after 60 seconds"
        except Exception as e:
            output = f"An error occurred: {str(e)}"
        
        return render_template('index.html', output=output)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
