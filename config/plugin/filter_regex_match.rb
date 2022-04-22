require 'fluent/plugin/filter'

module Fluent::Plugin
  class RegexMatchFilter < Filter
    # Register this filter as "passthru"
    Fluent::Plugin.register_filter('regex_match', self)

    # config_param works like other plugins
    config_param :match_paterns, :hash, default: {}, symbolize_keys: true, value_type: :regexp

    def filter(tag, time, record)
      # Since our example is a pass-thru filter, it does nothing and just
      # returns the record as-is.
      # If returns nil, that records are ignored.
      match_paterns.each do |key, regex|
        if regex.match? record["message"]
          record["match"] = {"type" => key, "vars" => {}}
          match = record["message"].match regex
          regex.names.each do |capture|
            record["match"]["vars"][capture] = match[capture]
          end
          return record
        end
      end

      nil
    end
  end
end
