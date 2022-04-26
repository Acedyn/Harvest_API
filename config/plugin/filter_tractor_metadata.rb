require 'fluent/plugin/filter'

module Fluent::Plugin
  class TractorMetadataFilter < Filter
    # Register this filter as "passthru"
    Fluent::Plugin.register_filter('tractor_metadata', self)

    def filter(tag, time, record)
      record["time"] = time
      record["file"] = tag

      filesplit = tag.split(".")
      record["user"] = filesplit[1]
      record["jid"] = filesplit[2]
      record["tid"] = filesplit[3]

      record
    end
  end
end
