<DOCTYPE HTML>
<html>
  <head>

    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>${hda.name | h} | ${visualization_name}</title>

    <title>Visualize your interactome</title>
    <% 
      root = h.url_for( '/static/' )
      app_root = root + 'plugins/visualizations/heatmap_visualization/static/'
                    %>

    <!-- Include here all JS and CSS scripts -->
    ${h.javascript_link( app_root + '')}

  </head>
  
  ## ----------------------------------------------------------------------------
  <body>

    <script>
    </script>

  </body>

</html>