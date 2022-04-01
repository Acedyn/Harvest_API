function process(event) {
  var logMessage = event.Get("message");

  if (!logMessage) {
    return;
  }

  var baseMatches = {
    "init-command": {
      regex: /^====\[(\d+\/\d+\/\d+ \d+\:\d+\:\d+).+ on (.+) \]====$/,
      groups: ["timestamp", "computer"],
    },
    "exit-command": {
      regex: /^====\[(\d+\/\d+\/\d+ \d+\:\d+\:\d+).+ exit code: (\d)\]====$/,
      groups: ["timestamp", "exit-code"],
    },
  };

  Object.keys(baseMatches).forEach(function (tag) {
    var regex = baseMatches[tag].regex;
    if (logMessage.match(regex)) {
      event.Tag(tag);
    }
  });
}
