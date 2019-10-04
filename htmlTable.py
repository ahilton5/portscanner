class Table:
    def __init__(self):
        self.title = ""
        self.rows = {}
        self.header = ""
    def __str__(self):
        s = "<h3>"
        s += self.title
        s += "</h3>"
        s += "<table class='report'>"
        s += self.header
        for r in self.rows.keys():
            s += "<tr>"
            s += "<td>"
            s += str(r)
            s += "</td>"
            for d in self.rows[r]:
                s += "<td>"
                s += d
                s += "</td>"
            s += "</tr>"
        s += "</table>"
        return s
    def setHeader(self, headers):
        r = "<tr>"
        r += "<th>Port</th>"
        for h in headers:
            r += "<th>" + h + "</th>"
        r += "</tr>"
        self.header = r
    def addEntry(self, port, result):
        port = int(port)
        if port in self.rows:
            self.rows[port].append(result)
        else:
            self.rows[port] = [result]