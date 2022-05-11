require 'fluent/plugin/filter'

module Fluent::Plugin
  class TractorMetadataFilter < Filter
    # Register this filter as "passthru"
    Fluent::Plugin.register_filter('tractor_metadata', self)

    def filter(tag, time, record)
      record["time"] = time
      record["file"] = tag

      filesplit = tag.split(".")
      record["user"] = filesplit[3]
      record["jid"] = filesplit[4]
      record["tid"] = filesplit[5]

      record
    end
  end
end
