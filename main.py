from geolite2 import geolite2
import pandas as pd
import geopandas
from matplotlib import pyplot as plt


with open("access.log") as f:
  log= f.read().split("\n")


location = []
reader = geolite2.reader()

for i,line in enumerate(log):
  log[i] = line.split(" ")[0]
  ip = reader.get(log[i])
  latitude = ip["location"]["latitude"]
  longitude = ip["location"]["longitude"]
  if ip != None:
    location.append({ "Longitude": longitude,"Latitude": latitude})

df = pd.DataFrame.from_dict(location)
gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
ax = world.plot(color=(.49,.49,.49), edgecolor=(.568,.568,.568),figsize=(14,7))

def plot(type="python"):
  if type == "python":
    ax.set_facecolor(color=(.31,.31,.31))

    gdf.plot(ax=ax, color='red',alpha=0.1)
    plt.tight_layout()
    plt.grid(True,c=(.5,.5,.5),linewidth=0.4)
    plt.show()

  elif type == "folium":
    import folium
    from folium.plugins import HeatMap
    hmap = folium.Map(location=[42.5, -75.5], zoom_start=7, )

    max_amount = max(set(log), key=log.count)
    hm_wide = HeatMap(list(zip(gdf.Latitude.values, gdf.Longitude.values,)),
       min_opacity=0.2,
       max_val=max_amount,
       radius=17, blur=15, 
       max_zoom=1, 
      )

    folium.GeoJson(world).add_to(hmap)
    hmap.add_child(hm_wide)

    import subprocess
    import webbrowser
    from http.server import BaseHTTPRequestHandler, HTTPServer


    PORT = 7000
    HOST = '127.0.0.1'
    SERVER_ADDRESS = '{host}:{port}'.format(host=HOST, port=PORT)
    FULL_SERVER_ADDRESS = 'http://' + SERVER_ADDRESS


    def TemproraryHttpServer(page_content_type, raw_data):
        """
        A simpe, temprorary http web server on the pure Python 3.
        It has features for processing pages with a XML or HTML content.
        """

        class HTTPServerRequestHandler(BaseHTTPRequestHandler):
            """
            An handler of request for the server, hosting XML-pages.
            """

            def do_GET(self):
                """Handle GET requests"""

                # response from page
                self.send_response(200)

                # set up headers for pages
                content_type = 'text/{0}'.format(page_content_type)
                self.send_header('Content-type', content_type)
                self.end_headers()

                # writing data on a page
                self.wfile.write(bytes(raw_data, encoding='utf'))

                return

        if page_content_type not in ['html', 'xml']:
            raise ValueError('This server can serve only HTML or XML pages.')

        page_content_type = page_content_type

        # kill a process, hosted on a localhost:PORT
        subprocess.call(['fuser', '-k', '{0}/tcp'.format(PORT)])

        # Started creating a temprorary http server.
        httpd = HTTPServer((HOST, PORT), HTTPServerRequestHandler)

        # run a temprorary http server
        httpd.serve_forever()


    def run_html_server(html_data=None):

        if html_data is None:
            html_data = """
            <!DOCTYPE html>
            <html>
            <head>
            <title>Page Title</title>
            </head>
            <body>
            <h1>This is a Heading</h1>
            <p>This is a paragraph.</p>
            </body>
            </html>
            """

        # open in a browser URL and see a result
        webbrowser.open(FULL_SERVER_ADDRESS)

        # run server
        TemproraryHttpServer('html', html_data)

    # ------------------------------------------------------------------------------------------------


    # now let's save the visualization into the temp file and render it
    from tempfile import NamedTemporaryFile
    tmp = NamedTemporaryFile()
    hmap.save(tmp.name)
    with open(tmp.name) as f:
        hmap_html = f.read()

    run_html_server(hmap_html)

plot(type="python")