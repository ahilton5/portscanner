<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" href="main.css"/>
  <meta name="viewport" content="width=device-width" />
  <link rel="icon" href="favicon.png">
  <title>Port Scanner</title>
  <script src="main.js"></script>
</head>
<body>
<div class='horizontal'>
    <section>
        <h2>Add Host</h2>
        <form action="/add_host">
            <table class='plain'>
                <tr>
                    <td>Host(s):</td>
                    <td><input name='host' placeholder='e.g. 192.0.2.1 or 192.0.2.0/24' required></td>
                </tr>
                <tr>
                    <td>Ports:</td>
                    <td><input name='ports' placeholder="e.g. 1-5,10. Leave empty for defaults."></td>
                </tr>
                <tr>
                    <td>Protocol:</td>
                    <td>
                        <select name='protocol'>
                            <option value="TCP">TCP</option>
                            <option value="UDP">UDP</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <td></td>
                    <td align="right"><button type="submit">Add</button></td>
                </tr>
            </table>
        </form>
        
    </section>
    <section style="min-height: 200px;">
        <h2>Planned Scan</h2>
        <table class='fancy'>
        <tr>
            <th width='200px'>Host(s)</th>
            <th width='200px'>Ports</th>
            <th width='100px'>Protocol</th>
        </tr>
        %for i in range(len(hosts)):
        <tr>
            <td title="{{', '.join(hosts[i]['hosts'])}}">{{hosts[i]['hostStr']}} <i>({{len(hosts[i]['hosts'])}} total)</i></td>
            <td title="{{', '.join([str(p) for p in hosts[i]['ports']])}}">{{hosts[i]['portsStr']}} <i>({{len(hosts[i]['ports'])}} total)</i></td>
            <td>{{hosts[i]['protocol']}}</td>
            <td class="invis"><form action="/delete_host"><input type="hidden" name="hostNum" value="{{i}}"><button type="submit">Delete</button></form></td>
        </tr>
        %end
        </table>
    </section>
    <section>
        <h2>Start Scan</h2>
        <form action="/start">
            <table class='plain'>
                <tr>
                    <td>{{total}} total ports will be scanned.</td>
                </tr>
                <tr>
                    <td>In the worst case scenario, this will take {{timeout}} second(s) per port.</td>
                </tr>
                <tr>
                    <td></td>
                    <td align="right"><button type="submit" style="background-color: green;">Start</button></td>
                </tr>
            </table>
        </form>
        %if started:
        <p>Scan Progress (see terminal output for more detailed progress):</p>
        <div id="Progress_Status"> 
            <div id="myprogressBar"></div> 
        </div>
        %else:
        <div id="Progress_Status" style="visibility: hidden;"> 
            <div id="myprogressBar"></div> 
        </div>
        %end
        <p id="finished-memo" style="visibility: hidden;">Finished. Results saved to <a href='{{saveto}}'>{{saveto}}</a>.</p>
    </section>
</div>
%for alert in alerts:
    <script>
        function myFunction() {
        alert("{{alert}}");
        }
        window.myFunction()
    </script>
%end
</body>
</html>
