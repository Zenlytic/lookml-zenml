- dashboard: funnel_conversion_data
  title: Funnel Conversion Data
  layout: newspaper
  preferred_viewer: dashboards-next
  elements:
  - title: Traffic by Channel
    name: Traffic by Channel
    model: testing_model
    explore: permanent_session
    type: looker_pie
    fields: [permanent_session.utm_source, permanent_session.count_distinct_sessions]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.utm_source: ''
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.utm_source]
    limit: 30
    dynamic_fields: [{measure: list_of_event, based_on: tracking_view.event, type: list,
        label: List of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {table_calculation: tof_conversion, label: TOF conversion,
        expression: "${user_view.count}/${permanent_session.count_distinct_sessions}",
        value_format: !!null '', value_format_name: !!null '', _kind_hint: measure,
        _type_hint: number, is_disabled: true}]
    query_timezone: America/Los_Angeles
    value_labels: legend
    label_type: labPer
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    defaults_version: 1
    series_types: {}
    hidden_fields:
    listen: {}
    row: 2
    col: 0
    width: 8
    height: 6
  - title: Mobile Users
    name: Mobile Users
    model: testing_model
    explore: permanent_session
    type: looker_pie
    fields: [permanent_session.is_mobile, permanent_session.count_distinct_sessions]
    fill_fields: [permanent_session.is_mobile]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.utm_source: ''
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.is_mobile]
    limit: 500
    dynamic_fields: [{measure: list_of_event, based_on: tracking_view.event, type: list,
        label: List of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {table_calculation: tof_conversion, label: TOF conversion,
        expression: "${user_view.count}/${permanent_session.count_distinct_sessions}",
        value_format: !!null '', value_format_name: !!null '', _kind_hint: measure,
        _type_hint: number, is_disabled: true}]
    query_timezone: America/Los_Angeles
    value_labels: legend
    label_type: labPer
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    defaults_version: 1
    series_types: {}
    hidden_fields:
    listen: {}
    row: 2
    col: 8
    width: 8
    height: 6
  - title: OS traffic
    name: OS traffic
    model: testing_model
    explore: permanent_session
    type: looker_donut_multiples
    fields: [permanent_session.operating_system, permanent_session.is_mobile,
      permanent_session.count_distinct_sessions]
    pivots: [permanent_session.operating_system]
    fill_fields: [permanent_session.is_mobile]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.utm_source: ''
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.count_distinct_sessions desc 0, permanent_session.is_mobile,
      permanent_session.operating_system]
    limit: 500
    dynamic_fields: [{measure: list_of_event, based_on: tracking_view.event, type: list,
        label: List of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}]
    query_timezone: America/Los_Angeles
    show_value_labels: true
    font_size: 12
    color_application:
      collection_id: 7c56cc2
      palette_id: 5d189dfc-4
      options:
        steps: 5
        reverse: false
    series_colors: {}
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    defaults_version: 1
    series_types: {}
    hidden_fields:
    value_labels: legend
    label_type: labPer
    ordering: none
    show_null_labels: false
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    listen: {}
    row: 2
    col: 16
    width: 8
    height: 6
  - title: TOF conversion by device type
    name: TOF conversion by device type
    model: testing_model
    explore: permanent_session
    type: looker_line
    fields: [user_view.count, permanent_session.is_mobile, permanent_session.session_date_date,
      permanent_session.count_distinct_sessions]
    pivots: [permanent_session.is_mobile]
    fill_fields: [permanent_session.is_mobile, permanent_session.session_date_date]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.utm_source: ''
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.is_mobile, permanent_session.session_date_date
        desc]
    limit: 500
    dynamic_fields: [{measure: list_of_event, based_on: tracking_view.event, type: list,
        label: List of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {category: table_calculation, expression: "${user_view.count}/${permanent_session.count_distinct_sessions}",
        label: TOF conversion, value_format: !!null '', value_format_name: percent_2,
        _kind_hint: measure, table_calculation: tof_conversion, _type_hint: number}]
    query_timezone: America/Los_Angeles
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    series_types: {}
    series_labels:
      No - tof_conversion: Non-mobile
      Yes - tof_conversion: Mobile
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    defaults_version: 1
    hidden_fields: [permanent_session.count_distinct_sessions, user_view.count,
      permanent_session.count_distinct_sessions]
    listen: {}
    row: 10
    col: 16
    width: 8
    height: 6
  - title: TOF conversion by channel
    name: TOF conversion by channel
    model: testing_model
    explore: permanent_session
    type: looker_line
    fields: [user_view.count, permanent_session.utm_source, permanent_session.count_distinct_sessions,
      permanent_session.session_date_date]
    pivots: [permanent_session.utm_source]
    fill_fields: [permanent_session.session_date_date]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.utm_source: fb,ig,google,reviews,instagram,snap,NULL
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.utm_source, permanent_session.session_date_date
        desc]
    limit: 500
    dynamic_fields: [{measure: list_of_event, based_on: tracking_view.event, type: list,
        label: List of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {category: table_calculation, expression: "${user_view.count}/${permanent_session.count_distinct_sessions}",
        label: TOF conversion, value_format: !!null '', value_format_name: percent_2,
        _kind_hint: measure, table_calculation: tof_conversion, _type_hint: number}]
    query_timezone: America/Los_Angeles
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    color_application:
      collection_id: b43731d5-dc87-4a
      palette_id: fb7bb53e-b77
      options:
        steps: 5
    series_types: {}
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    defaults_version: 1
    hidden_fields: [permanent_session.count_distinct_sessions, user_view.count,
      permanent_session.count_distinct_sessions]
    listen: {}
    row: 10
    col: 8
    width: 8
    height: 6
  - title: TOF conversion
    name: TOF conversion
    model: testing_model
    explore: permanent_session
    type: looker_line
    fields: [user_view.count, permanent_session.count_distinct_sessions,
      permanent_session.session_date_date]
    fill_fields: [permanent_session.session_date_date]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.session_date_date desc]
    limit: 500
    dynamic_fields: [{measure: list_of_event, based_on: tracking_view.event, type: list,
        label: List of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {category: table_calculation, expression: "${user_view.count}/${permanent_session.count_distinct_sessions}",
        label: TOF conversion, value_format: !!null '', value_format_name: percent_2,
        _kind_hint: measure, table_calculation: tof_conversion, _type_hint: number}]
    query_timezone: America/Los_Angeles
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    color_application:
      collection_id: b43731d5-dc87-
      palette_id: fb7bb53e-b77b-
      options:
        steps: 5
    series_types: {}
    series_colors:
      tof_conversion: "#B1399E"
    reference_lines: [{reference_type: line, line_value: mean, range_start: max, range_end: min,
        margin_top: deviation, margin_value: mean, margin_bottom: deviation, label_position: center,
        color: "#000000"}]
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    value_format: 0.0%
    conditional_formatting: [{type: equal to, value: !!null '', background_color: !!null '',
        font_color: !!null '', color_application: {collection_id: b43731d5-dc87-4a8e-b807,
          palette_id: 1e4d66b9-f066-4c33-}, bold: false, italic: false,
        strikethrough: false, fields: !!null ''}]
    defaults_version: 1
    hidden_fields: [permanent_session.count_distinct_sessions, user_view.count,
      permanent_session.count_distinct_sessions]
    listen: {}
    row: 10
    col: 0
    width: 8
    height: 6
  - title: Overall Conversion
    name: Overall Conversion
    model: testing_model
    explore: permanent_session
    type: looker_line
    fields: [user_view.count, profiles_orders_view.order_count, permanent_session.count_distinct_sessions,
      permanent_session.session_date_date]
    fill_fields: [permanent_session.session_date_date]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.session_date_date desc]
    limit: 500
    dynamic_fields: [{measure: list_of_event, based_on: tracking_view.event, type: list,
        label: List of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {category: table_calculation, expression: "${profiles_orders_view.order_count}/${permanent_session.count_distinct_sessions}",
        label: Overall conversion, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: overall_conversion, _type_hint: number}]
    query_timezone: America/Los_Angeles
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    color_application:
      collection_id: esfvgbfesfeqsf
      palette_id: fsaegrsfada
      options:
        steps: 5
    series_types: {}
    reference_lines: [{reference_type: line, line_value: mean, range_start: max, range_end: min,
        margin_top: deviation, margin_value: mean, margin_bottom: deviation, label_position: center,
        color: "#000000", label: ''}]
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    value_format: 0.0%
    conditional_formatting: [{type: equal to, value: !!null '', background_color: !!null '',
        font_color: !!null '', color_application: {collection_id: b43731d5-dc87-4a,
          palette_id: 1e4d66b9-f066}, bold: false, italic: false,
        strikethrough: false, fields: !!null ''}]
    defaults_version: 1
    hidden_fields: [permanent_session.count_distinct_sessions, user_view.count,
      profiles_orders_view.order_count, permanent_session.count_distinct_sessions]
    listen: {}
    row: 16
    col: 0
    width: 8
    height: 5
  - title: TOF conversion percentage
    name: TOF conversion percentage
    model: testing_model
    explore: permanent_session
    type: looker_column
    fields: [quiz_start_1, quiz_complete, user_view.count, permanent_session.session_date_date,
      permanent_session.count_distinct_sessions]
    fill_fields: [permanent_session.session_date_date]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.session_date_date desc]
    limit: 500
    dynamic_fields: [{category: table_calculation, expression: "${permanent_session.count_distinct_sessions}/${permanent_session.count_distinct_sessions}",
        label: Start, value_format: !!null '', value_format_name: percent_1, _kind_hint: measure,
        table_calculation: start, _type_hint: number}, {category: table_calculation,
        expression: "${quiz_start_1}/${permanent_session.count_distinct_sessions}",
        label: Quiz Start %, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: quiz_start, _type_hint: number}, {
        category: table_calculation, expression: "${quiz_complete}/${permanent_session.count_distinct_sessions}",
        label: Quiz Finish %, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: quiz_finish, _type_hint: number},
      {category: table_calculation, expression: "${user_view.count}/${permanent_session.count_distinct_sessions}",
        label: Signup (give email), value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: signup_give_email, _type_hint: number},
      {measure: list_of_event, based_on: tracking_view.event, type: list, label: List
          of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {category: measure, expression: '${tracking_view.event}
          = "Quiz Start" OR (${tracking_view.event}="Page View" AND contains(${tracking_view.properties},
          "quiz"))', label: Quiz Start, value_format: !!null '', value_format_name: !!null '',
        based_on: permanent_session.count_distinct_sessions, filter_expression: '${tracking_view.event}
          = "Quiz Start" OR (${tracking_view.event}="Page View" AND contains(${tracking_view.properties},
          "quiz"))', _kind_hint: measure, measure: quiz_start_1, type: count_distinct,
        _type_hint: number}, {category: measure, expression: '${tracking_view.event}
          = "Quiz complete"', label: Quiz Complete, value_format: !!null '', value_format_name: !!null '',
        based_on: permanent_session.count_distinct_sessions, filter_expression: '${tracking_view.event}
          = "Quiz complete"', _kind_hint: measure, measure: quiz_complete, type: count_distinct,
        _type_hint: number}]
    query_timezone: America/Los_Angeles
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    ordering: none
    show_null_labels: false
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    leftAxisLabelVisible: false
    leftAxisLabel: ''
    rightAxisLabelVisible: false
    rightAxisLabel: ''
    color_application:
      collection_id: b43731d5-dc87-4a
      palette_id: fb7bb53e-b77b-4ab6-
      options:
        steps: 5
    smoothedBars: true
    orientation: automatic
    labelPosition: left
    percentType: total
    percentPosition: inline
    valuePosition: right
    labelColorEnabled: false
    labelColor: "#FFF"
    series_types: {}
    show_dropoff: true
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    value_format: 0.0%
    conditional_formatting: [{type: equal to, value: !!null '', background_color: !!null '',
        font_color: !!null '', color_application: {collection_id: b43731d5-dc87-4,
          palette_id: 1e4d66b9-f066-4c33-}, bold: false, italic: false,
        strikethrough: false, fields: !!null ''}]
    show_null_points: true
    interpolation: linear
    defaults_version: 1
    hidden_fields: [permanent_session.count_distinct_sessions, quiz_complete, user_view.count,
      quiz_start_2]
    listen: {}
    row: 31
    col: 0
    width: 9
    height: 7
  - title: TOF funnel by experience
    name: TOF funnel by experience
    model: testing_model
    explore: permanent_session
    type: looker_column
    fields: [quiz_start_1, quiz_complete, user_view.count, permanent_session.count_distinct_sessions,
      permanent_session.session_date_date, grouped_sessions_view.group]
    pivots: [grouped_sessions_view.group]
    fill_fields: [permanent_session.session_date_date]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.session_date_date desc, grouped_sessions_view.group]
    limit: 500
    dynamic_fields: [{category: table_calculation, expression: "${permanent_session.count_distinct_sessions}/${permanent_session.count_distinct_sessions}",
        label: Start, value_format: !!null '', value_format_name: percent_1, _kind_hint: measure,
        table_calculation: start, _type_hint: number}, {category: table_calculation,
        expression: "${quiz_start_1}/${permanent_session.count_distinct_sessions}",
        label: Quiz Start %, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: quiz_start, _type_hint: number}, {
        category: table_calculation, expression: "${quiz_complete}/${permanent_session.count_distinct_sessions}",
        label: Quiz Finish %, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: quiz_finish, _type_hint: number},
      {category: table_calculation, expression: "${user_view.count}/${permanent_session.count_distinct_sessions}",
        label: Signup (give email), value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: signup_give_email, _type_hint: number},
      {measure: list_of_event, based_on: tracking_view.event, type: list, label: List
          of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {category: measure, expression: '${tracking_view.event}
          = "Quiz Start" OR (${tracking_view.event}="Page View" AND contains(${tracking_view.properties},
          "quiz"))', label: Quiz Start, value_format: !!null '', value_format_name: !!null '',
        based_on: permanent_session.count_distinct_sessions, filter_expression: '${tracking_view.event}
          = "Quiz Start" OR (${tracking_view.event}="Page View" AND contains(${tracking_view.properties},
          "quiz"))', _kind_hint: measure, measure: quiz_start_1, type: count_distinct,
        _type_hint: number}, {category: measure, expression: '${tracking_view.event}
          = "Quiz complete"', label: Quiz Complete, value_format: !!null '', value_format_name: !!null '',
        based_on: permanent_session.count_distinct_sessions, filter_expression: '${tracking_view.event}
          = "Quiz complete"', _kind_hint: measure, measure: quiz_complete, type: count_distinct,
        _type_hint: number}]
    query_timezone: America/Los_Angeles
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: pivot
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    ordering: none
    show_null_labels: false
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    color_application:
      collection_id: esfvgbfesfeqsf
      palette_id: fsaegrsfada
      options:
        steps: 5
    y_axes: [{label: !!null '', orientation: left, series: [{axisId: quiz_start_1,
            id: top_sku_only - quiz_start_1, name: top_sku_only - Quiz Start}, {axisId: quiz_start_1,
            id: grouped_sessions_view.group___null - quiz_start_1, name: "∅\
              \ - Quiz Start"}, {axisId: start, id: top_sku_only - start, name: top_sku_only
              - Start}, {axisId: start, id: grouped_sessions_view.group___null
              - start, name: "∅ - Start"}, {axisId: quiz_start, id: top_sku_only -
              quiz_start, name: top_sku_only - Quiz Start %}, {axisId: quiz_start,
            id: grouped_sessions_view.group___null - quiz_start, name: "∅\
              \ - Quiz Start %"}, {axisId: quiz_finish, id: top_sku_only - quiz_finish,
            name: top_sku_only - Quiz Finish %}, {axisId: quiz_finish, id: grouped_sessions_view.group___null
              - quiz_finish, name: "∅ - Quiz Finish %"}, {axisId: signup_give_email,
            id: top_sku_only - signup_give_email, name: top_sku_only - Signup (give
              email)}, {axisId: signup_give_email, id: grouped_sessions_view.group___null
              - signup_give_email, name: "∅ - Signup (give email)"}], showLabels: true,
        showValues: true, unpinAxis: false, tickDensity: default, tickDensityCustom: 5,
        type: linear}]
    limit_displayed_rows_values:
      show_hide: hide
      first_last: first
      num_rows: 0
    hide_legend: false
    trellis_rows: 2
    series_types: {}
    show_dropoff: true
    leftAxisLabelVisible: false
    leftAxisLabel: ''
    rightAxisLabelVisible: false
    rightAxisLabel: ''
    smoothedBars: true
    orientation: automatic
    labelPosition: left
    percentType: total
    percentPosition: inline
    valuePosition: right
    labelColorEnabled: false
    labelColor: "#FFF"
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    value_format: 0.0%
    conditional_formatting: [{type: equal to, value: !!null '', background_color: !!null '',
        font_color: !!null '', color_application: {collection_id: esfvgbfesfeqsf,
          palette_id: ewf3r13rwf}, bold: false, italic: false,
        strikethrough: false, fields: !!null ''}]
    show_null_points: true
    interpolation: linear
    defaults_version: 1
    hidden_fields: [permanent_session.count_distinct_sessions, quiz_complete, user_view.count,
      quiz_start_2, permanent_session.count_distinct_sessions]
    listen: {}
    row: 31
    col: 9
    width: 15
    height: 7
  - title: TOF conversion funnel by channel
    name: TOF conversion funnel by channel
    model: testing_model
    explore: permanent_session
    type: looker_grid
    fields: [quiz_start_1, quiz_complete, user_view.count, permanent_session.utm_source,
      permanent_session.count_distinct_sessions, permanent_session.session_date_date]
    pivots: [permanent_session.utm_source]
    fill_fields: [permanent_session.session_date_date]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      grouped_sessions_view.group: 'NULL'
      permanent_session.utm_source: ig,google,fb,NULL
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.utm_source, permanent_session.session_date_date
        desc]
    limit: 500
    dynamic_fields: [{category: table_calculation, expression: "${permanent_session.count_distinct_sessions}/${permanent_session.count_distinct_sessions}",
        label: Start, value_format: !!null '', value_format_name: percent_1, _kind_hint: measure,
        table_calculation: start, _type_hint: number}, {category: table_calculation,
        expression: "${quiz_start_1}/${permanent_session.count_distinct_sessions}",
        label: Quiz Start %, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: quiz_start, _type_hint: number}, {
        category: table_calculation, expression: "${quiz_complete}/${permanent_session.count_distinct_sessions}",
        label: Quiz Finish %, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: quiz_finish, _type_hint: number},
      {category: table_calculation, expression: "${user_view.count}/${permanent_session.count_distinct_sessions}",
        label: Signup (give email), value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: signup_give_email, _type_hint: number},
      {measure: list_of_event, based_on: tracking_view.event, type: list, label: List
          of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {category: measure, expression: '${tracking_view.event}
          = "Quiz Start" OR (${tracking_view.event}="Page View" AND contains(${tracking_view.properties},
          "quiz"))', label: Quiz Start, value_format: !!null '', value_format_name: !!null '',
        based_on: permanent_session.count_distinct_sessions, filter_expression: '${tracking_view.event}
          = "Quiz Start" OR (${tracking_view.event}="Page View" AND contains(${tracking_view.properties},
          "quiz"))', _kind_hint: measure, measure: quiz_start_1, type: count_distinct,
        _type_hint: number}, {category: measure, expression: '${tracking_view.event}
          = "Quiz complete"', label: Quiz Complete, value_format: !!null '', value_format_name: !!null '',
        based_on: permanent_session.count_distinct_sessions, filter_expression: '${tracking_view.event}
          = "Quiz complete"', _kind_hint: measure, measure: quiz_complete, type: count_distinct,
        _type_hint: number}]
    query_timezone: America/Los_Angeles
    show_view_names: false
    show_row_numbers: true
    transpose: false
    truncate_text: true
    hide_totals: false
    hide_row_totals: false
    size_to_fit: true
    table_theme: white
    limit_displayed_rows: false
    enable_conditional_formatting: false
    header_text_alignment: left
    header_font_size: '12'
    rows_font_size: '12'
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    color_application:
      collection_id: esfvgbfesfeqsf
      palette_id: fsaegrsfada
      options:
        steps: 5
    show_sql_query_menu_options: false
    show_totals: true
    show_row_totals: true
    series_cell_visualizations:
      quiz_start_1:
        is_active: false
      signup_give_email:
        is_active: true
    limit_displayed_rows_values:
      show_hide: hide
      first_last: first
      num_rows: 0
    conditional_formatting: [{type: equal to, value: !!null '', background_color: !!null '',
        font_color: !!null '', color_application: {collection_id: esfvgbfesfeqsf,
          palette_id: ewf3r13rwf}, bold: false, italic: false,
        strikethrough: false, fields: !!null ''}]
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: pivot
    stacking: ''
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    ordering: none
    show_null_labels: false
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    hide_legend: false
    trellis_rows: 2
    series_types: {}
    show_dropoff: true
    leftAxisLabelVisible: false
    leftAxisLabel: ''
    rightAxisLabelVisible: false
    rightAxisLabel: ''
    smoothedBars: true
    orientation: automatic
    labelPosition: left
    percentType: total
    percentPosition: inline
    valuePosition: right
    labelColorEnabled: false
    labelColor: "#FFF"
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    value_format: 0.0%
    show_null_points: true
    interpolation: linear
    defaults_version: 1
    hidden_fields: [permanent_session.count_distinct_sessions, quiz_complete, user_view.count,
      quiz_start_2]
    listen: {}
    row: 38
    col: 0
    width: 24
    height: 9
  - title: Overall TOF conversion by channel
    name: Overall TOF conversion by channel
    model: testing_model
    explore: permanent_session
    type: looker_grid
    fields: [user_view.count, permanent_session.utm_source, permanent_session.session_date_date,
      permanent_session.count_distinct_sessions]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.utm_source: fb,ig,reviews,google,NULL
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.session_date_date desc]
    limit: 500
    dynamic_fields: [{measure: list_of_event, based_on: tracking_view.event, type: list,
        label: List of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {category: table_calculation, expression: "${user_view.count}/${permanent_session.count_distinct_sessions}",
        label: TOF conversion, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: tof_conversion, _type_hint: number}]
    query_timezone: America/Los_Angeles
    show_view_names: false
    show_row_numbers: true
    transpose: false
    truncate_text: true
    hide_totals: false
    hide_row_totals: false
    size_to_fit: true
    table_theme: gray
    limit_displayed_rows: false
    enable_conditional_formatting: false
    header_text_alignment: left
    header_font_size: '12'
    rows_font_size: '12'
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    color_application:
      collection_id: esfvgbfesfeqsf
      palette_id: fsaegrsfada
      options:
        steps: 5
    show_sql_query_menu_options: false
    show_totals: true
    show_row_totals: true
    series_labels: {}
    series_cell_visualizations:
      tof_conversion:
        is_active: true
        palette:
          palette_id: 471a8295-662d-46fc-bd2d-2d0acd370c1e
          collection_id: esfvgbfesfeqsf
    conditional_formatting: [{type: equal to, value: !!null '', background_color: !!null '',
        font_color: !!null '', color_application: {collection_id: esfvgbfesfeqsf,
          palette_id: ewf3r13rwf}, bold: false, italic: false,
        strikethrough: false, fields: !!null ''}]
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    value_format: 0.0%
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    legend_position: center
    series_types: {}
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    defaults_version: 1
    hidden_fields: [permanent_session.count_distinct_sessions, user_view.count,
      permanent_session.count_distinct_sessions]
    hidden_points_if_no: []
    ordering: none
    show_null_labels: false
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    font_size: 12
    bar_range_max: 1
    range_max: 1
    groupBars: true
    labelSize: 10pt
    showLegend: true
    truncate_column_names: false
    listen: {}
    row: 16
    col: 16
    width: 8
    height: 5
  - name: Conversion Rates
    type: text
    title_text: Conversion Rates
    subtitle_text: Over last 7 days
    body_text: ''
    row: 8
    col: 0
    width: 24
    height: 2
  - name: Funnel Analysis
    type: text
    title_text: Funnel Analysis
    subtitle_text: Over last 7 days
    body_text: ''
    row: 29
    col: 0
    width: 24
    height: 2
  - name: User Demographics
    type: text
    title_text: User Demographics
    subtitle_text: Over last 7 days
    body_text: ''
    row: 0
    col: 0
    width: 24
    height: 2
  - title: Overall Conversion by Channel
    name: Overall Conversion by Channel
    model: testing_model
    explore: permanent_session
    type: looker_grid
    fields: [user_view.count, profiles_orders_view.order_count, permanent_session.utm_source,
      permanent_session.count_distinct_sessions, permanent_session.session_date_date]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      permanent_session.utm_source: fb,ig,google,reviews,NULL
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.session_date_date desc]
    limit: 500
    dynamic_fields: [{measure: list_of_event, based_on: tracking_view.event, type: list,
        label: List of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {category: table_calculation, expression: "${profiles_orders_view.order_count}/${permanent_session.count_distinct_sessions}",
        label: Overall conversion, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: overall_conversion, _type_hint: number}]
    query_timezone: America/Los_Angeles
    show_view_names: false
    show_row_numbers: true
    transpose: false
    truncate_text: true
    hide_totals: false
    hide_row_totals: false
    size_to_fit: true
    table_theme: white
    limit_displayed_rows: false
    enable_conditional_formatting: false
    header_text_alignment: left
    header_font_size: '12'
    rows_font_size: '12'
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    color_application:
      collection_id: esfvgbfesfeqsf
      palette_id: fsaegrsfada
      options:
        steps: 5
    show_sql_query_menu_options: false
    show_totals: true
    show_row_totals: true
    series_cell_visualizations:
      overall_conversion:
        is_active: true
    conditional_formatting: [{type: equal to, value: !!null '', background_color: !!null '',
        font_color: !!null '', color_application: {collection_id: esfvgbfesfeqsf,
          palette_id: ewf3r13rwf}, bold: false, italic: false,
        strikethrough: false, fields: !!null ''}]
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    series_types: {}
    reference_lines: [{reference_type: line, line_value: mean, range_start: max, range_end: min,
        margin_top: deviation, margin_value: mean, margin_bottom: deviation, label_position: center,
        color: "#000000", label: ''}]
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    value_format: 0.0%
    defaults_version: 1
    hidden_fields: [permanent_session.count_distinct_sessions, user_view.count,
      profiles_orders_view.order_count]
    listen: {}
    row: 16
    col: 8
    width: 8
    height: 5
  - title: Conversion funnel by channel L7
    name: Conversion funnel by channel L7
    model: testing_model
    explore: permanent_session
    type: looker_grid
    fields: [quiz_start_1, quiz_complete, user_view.count, permanent_session.utm_source,
      user_view.overall_bottom_of_funnel_conversion, permanent_session.session_date_date,
      permanent_session.count_distinct_sessions]
    pivots: [permanent_session.utm_source]
    fill_fields: [permanent_session.session_date_date]
    filters:
      permanent_session.is_bot: 'No'
      permanent_session.entry_page: "-%users%,-%login%,-%checkout%,-%me%"
      user_view.date_joined_date: 7 days ago for 7 days,NULL
      grouped_sessions_view.group: 'NULL'
      permanent_session.utm_source: ig,fb,NULL
      permanent_session.session_date_date: 7 days ago for 7 days
    sorts: [permanent_session.utm_source, permanent_session.session_date_date
        desc]
    limit: 500
    dynamic_fields: [{category: table_calculation, expression: "${permanent_session.count_distinct_sessions}/${permanent_session.count_distinct_sessions}",
        label: Start, value_format: !!null '', value_format_name: percent_1, _kind_hint: measure,
        table_calculation: start, _type_hint: number}, {category: table_calculation,
        expression: "${quiz_start_1}/${permanent_session.count_distinct_sessions}",
        label: Quiz Start %, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: quiz_start, _type_hint: number}, {
        category: table_calculation, expression: "${quiz_complete}/${permanent_session.count_distinct_sessions}",
        label: Quiz Finish %, value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: quiz_finish, _type_hint: number},
      {category: table_calculation, expression: "${user_view.count}/${permanent_session.count_distinct_sessions}",
        label: Signup (give email), value_format: !!null '', value_format_name: percent_1,
        _kind_hint: measure, table_calculation: signup_give_email, _type_hint: number},
      {measure: list_of_event, based_on: tracking_view.event, type: list, label: List
          of Event, expression: !!null '', _kind_hint: measure, _type_hint: list},
      {dimension: page_view, label: Page View, expression: '${tracking_view.event}
          = "Page View"', value_format: !!null '', value_format_name: !!null '', _kind_hint: dimension,
        _type_hint: yesno}, {category: measure, expression: '${tracking_view.event}
          = "Quiz Start" OR (${tracking_view.event}="Page View" AND contains(${tracking_view.properties},
          "quiz"))', label: Quiz Start, value_format: !!null '', value_format_name: !!null '',
        based_on: permanent_session.count_distinct_sessions, filter_expression: '${tracking_view.event}
          = "Quiz Start" OR (${tracking_view.event}="Page View" AND contains(${tracking_view.properties},
          "quiz"))', _kind_hint: measure, measure: quiz_start_1, type: count_distinct,
        _type_hint: number}, {category: measure, expression: '${tracking_view.event}
          = "Quiz complete"', label: Quiz Complete, value_format: !!null '', value_format_name: !!null '',
        based_on: permanent_session.count_distinct_sessions, filter_expression: '${tracking_view.event}
          = "Quiz complete"', _kind_hint: measure, measure: quiz_complete, type: count_distinct,
        _type_hint: number}]
    query_timezone: America/Los_Angeles
    show_view_names: false
    show_row_numbers: true
    transpose: false
    truncate_text: true
    hide_totals: false
    hide_row_totals: false
    size_to_fit: true
    table_theme: white
    limit_displayed_rows: false
    enable_conditional_formatting: false
    header_text_alignment: left
    header_font_size: '12'
    rows_font_size: '12'
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    color_application:
      collection_id: esfvgbfesfeqsf
      palette_id: fsaegrsfada
      options:
        steps: 5
    show_sql_query_menu_options: false
    show_totals: true
    show_row_totals: true
    series_cell_visualizations:
      quiz_start_1:
        is_active: false
      signup_give_email:
        is_active: true
    limit_displayed_rows_values:
      show_hide: hide
      first_last: first
      num_rows: 0
    conditional_formatting: [{type: equal to, value: !!null '', background_color: !!null '',
        font_color: !!null '', color_application: {collection_id: esfvgbfesfeqsf,
          palette_id: ewf3r13rwf}, bold: false, italic: false,
        strikethrough: false, fields: !!null ''}]
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: pivot
    stacking: ''
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    ordering: none
    show_null_labels: false
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    hide_legend: false
    trellis_rows: 2
    series_types: {}
    show_dropoff: true
    leftAxisLabelVisible: false
    leftAxisLabel: ''
    rightAxisLabelVisible: false
    rightAxisLabel: ''
    smoothedBars: true
    orientation: automatic
    labelPosition: left
    percentType: total
    percentPosition: inline
    valuePosition: right
    labelColorEnabled: false
    labelColor: "#FFF"
    custom_color_enabled: true
    show_single_value_title: true
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    value_format: 0.0%
    show_null_points: true
    interpolation: linear
    defaults_version: 1
    hidden_fields: [permanent_session.count_distinct_sessions, quiz_complete, user_view.count,
      quiz_start_2]
    listen: {}
    row: 47
    col: 0
    width: 24
    height: 6