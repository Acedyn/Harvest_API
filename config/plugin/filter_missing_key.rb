require 'fluent/plugin/filter'

module Fluent::Plugin
  class MissingKeyFilter < Filter
    # Register this filter as "passthru"
    Fluent::Plugin.register_filter('missing_key', self)

    config_param :key_name, :string

    def filter(tag, time, record)
      unless record.key?(key_name)
        return nil
      end

      record
    end
  end
end
