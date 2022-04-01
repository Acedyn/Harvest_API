function process(event) {
  var filePath = event.Get("log.file.path");

  if (!filePath) {
    return;
  }

  var splittedPath = filePath.split("/");
  var jid = splittedPath[splittedPath.length - 2];
  var name = splittedPath[splittedPath.length - 1];
  var tid = name.split(".")[0];

  event.Put("tractor.jid", jid.substring(1));
  event.Put("tractor.tid", tid.substring(1));
}
