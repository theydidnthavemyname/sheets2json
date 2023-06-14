To get a google sheet's url, in the document go to File > Share > Publish to web. Be sure to select a specific sheet if there are multiple, Google will only output the first one if you choose Entire Document.

Add the urls to sheets.json as "name":"url" (don't forget to add commas for any item before the last). Set the output path for your generated json files under "output_path" (it's "output\" by default - don't forget to escape backslashes).

In the sheets themselves, the first row is used as headers, so label them appropriately.