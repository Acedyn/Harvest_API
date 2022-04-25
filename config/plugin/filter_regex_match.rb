require 'fluent/plugin/filter'

module Fluent::Plugin
  class RegexMatchFilter < Filter
    # Register this filter as "passthru"
    Fluent::Plugin.register_filter('regex_match', self)

    # config_param works like other plugins
    config_param :match_patern, :regexp
    config_param :match_name, :string
    config_param :help_message, :string, default: ""

    def filter(tag, time, record)
      if record["message"].match?(match_patern)
        record["match"] = {"type" => match_name, "vars" => {}}
        match = record["message"].match(match_patern)

        match_patern.names.each do |capture|
          record["match"]["vars"][capture] = match[capture]
        end

        if help_message != ""
          record["match"]["vars"].default = "none"
          record["match"]["help"] = help_message % record["match"]["vars"].transform_keys(&:to_sym)
        end
      end
      
      record
    end
  end
end
