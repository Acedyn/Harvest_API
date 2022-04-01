function process(event) {
  var logMessage = event.Get("message");

  if (!logMessage) {
    return;
  }

  var baseMatches = {
    "ram-error": {
      regex: /^Memory allocation failure;/,
      groups: [],
    },
    "license-error": {
      regex: /Could not obtain a license/,
      groups: [],
    },
    "image-write": {
      regex: /Successfully written image file "(.+)"$/,
      groups: ["image-path"],
    },
    "missing-vrscene": {
      regex: /No file "(P:\\.+.vrscene)" exists$/,
      groups: ["vrscene-path"],
    },
  };

  Object.keys(baseMatches).forEach(function (tag) {
    var regex = baseMatches[tag].regex;
    if (logMessage.match(regex)) {
      tag = "vrscene-" + tag;
      event.Tag(tag);
    }
  });
}
