- dashboard: conversion_rates
  title: Conversion Rates
  layout: newspaper
  preferred_viewer: dashboards-next
  elements:
  - name: Quiz Start Rates
    title: Quiz Start Rates
    merged_queries:
    - model: testing_model
      explore: permanent_session_view
      type: looker_line
      fields: [permanent_session_view.count_distinct_sessions, permanent_session_view.session_date_month]
      fill_fields: [permanent_session_view.session_date_month]
      filters:
        permanent_session_view.session_date_date: "12 months ago for 12 months"
        permanent_session_view.entry_page: "-%blog%"
        permanent_session_view.is_bot: 'No'
      sorts: [permanent_session_view.session_date_month desc]
      limit: 500
      filter_expression: "if(is_null(${user_view.date_joined_time}), now(),\n\
        \  ${user_view.date_joined_time}) > ${permanent_session_view.session_date_week} "
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
      defaults_version: 1
      join_fields: []
    - model: testing_model
      explore: visitors_view
      type: table
      fields: [visitors_view.session_time_month, visitors_view.total_quiz_starts]
      fill_fields: [visitors_view.session_time_month]
      filters:
        visitors_view.session_time_date: 12 months ago for 12 months
        visitors_view.entry_page: "-%blog%"
        visitors_view.is_bot: 'No'
      sorts: [visitors_view.session_time_month desc]
      limit: 500
      query_timezone: America/Los_Angeles
      join_fields:
      - field_name: visitors_view.session_time_month
        source_field_name: permanent_session_view.session_date_month
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    y_axes: [{label: '', orientation: left, series: [{axisId: permanent_session_view.distinct_sessions,
            id: permanent_session_view.distinct_sessions, name: Distinct Sessions}],
        showLabels: true, showValues: true, unpinAxis: false, tickDensity: default,
        type: linear}, {label: !!null '', orientation: right, series: [{axisId: orders_conversion,
            id: orders_conversion, name: Orders Conversion}], showLabels: true, showValues: true,
        unpinAxis: false, tickDensity: default, type: linear}]
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
    series_types: {}
    point_style: none
    series_colors:
      orders_conversion: "#E52592"
    show_value_labels: true
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    custom_color_enabled: true
    show_single_value_title: true
    single_value_title: Quiz Start Rate
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    hidden_fields: [visitors_view.total_quiz_starts, profiles_orders.count,
      consultationrates.total_quiz_finishes, visitors_view.quiz_finish_rate_by_distinct_sessions,
      visitors_view.quiz_start_rate, user_view.bottom_of_funnel_conversion_within_24_hours,
      permanent_session_view.distinct_sessions, permanent_session_view.count_distinct_sessions]
    type: looker_line
    series_column_widths:
      user_view.bottom_of_funnel_conversion_within_24_hours: 143
    sorts: [visitors_view.session_time_week]
    dynamic_fields: [{category: table_calculation, expression: "${visitors_view.total_quiz_starts}\
          \ /${permanent_session_view.count_distinct_sessions}", label: Quiz  Start
          Rate, value_format: !!null '', value_format_name: percent_2, _kind_hint: measure,
        table_calculation: quiz_start_rate, _type_hint: number}]
    row: 0
    col: 0
    width: 24
    height: 7
  - name: Email Capture Rate
    title: Email Capture Rate
    merged_queries:
    - model: testing_model
      explore: permanent_session_view
      type: looker_line
      fields: [permanent_session_view.count_distinct_sessions, permanent_session_view.session_date_month]
      fill_fields: [permanent_session_view.session_date_month]
      filters:
        permanent_session_view.session_date_date: 12 months ago for 12 months
        permanent_session_view.entry_page: "-%blog%"
        permanent_session_view.is_bot: 'No'
      sorts: [permanent_session_view.session_date_month desc]
      limit: 500
      filter_expression: "if(is_null(${user_view.date_joined_time}), now(),\n\
        \  ${user_view.date_joined_time}) > ${permanent_session_view.session_date_week} "
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
      defaults_version: 1
      join_fields: []
    - model: testing_model
      explore: visitors_view
      type: table
      fields: [visitors_view.session_time_month, visitors_view.total_quiz_starts,
        visitors_view.total_quiz_finishes]
      fill_fields: [visitors_view.session_time_month]
      filters:
        visitors_view.session_time_date: 12 months ago for 12 months
        visitors_view.entry_page: "-%blog%"
        visitors_view.is_bot: 'No'
      sorts: [visitors_view.session_time_month desc]
      limit: 500
      query_timezone: America/Los_Angeles
      join_fields:
      - field_name: visitors_view.session_time_month
        source_field_name: permanent_session_view.session_date_month
    color_application:
      collection_id: qef2q3dw
      palette_id: be92eae
      options:
        steps: 5
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    y_axes: [{label: '', orientation: left, series: [{axisId: permanent_session_view.distinct_sessions,
            id: permanent_session_view.distinct_sessions, name: Distinct Sessions}],
        showLabels: true, showValues: true, unpinAxis: false, tickDensity: default,
        type: linear}, {label: !!null '', orientation: right, series: [{axisId: orders_conversion,
            id: orders_conversion, name: Orders Conversion}], showLabels: true, showValues: true,
        unpinAxis: false, tickDensity: default, type: linear}]
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
    series_types: {}
    point_style: none
    series_colors:
      email_capture_rate: "#D978A1"
    show_value_labels: true
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    custom_color_enabled: true
    show_single_value_title: true
    single_value_title: Quiz Start Rate
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    hidden_fields: [visitors_view.total_quiz_starts, profiles_orders.count,
      consultationrates.total_quiz_finishes, visitors_view.quiz_finish_rate_by_distinct_sessions,
      visitors_view.quiz_start_rate, user_view.bottom_of_funnel_conversion_within_24_hours,
      permanent_session_view.distinct_sessions, permanent_session_view.count_distinct_sessions,
      visitors_view.total_quiz_finishes, quiz_start_rate]
    type: looker_line
    series_column_widths:
      user_view.bottom_of_funnel_conversion_within_24_hours: 143
    sorts: [visitors_view.session_time_week]
    dynamic_fields: [{category: table_calculation, expression: "${visitors_view.total_quiz_starts}\
          \ /${permanent_session_view.count_distinct_sessions}", label: Quiz  Start
          Rate, value_format: !!null '', value_format_name: percent_2, _kind_hint: measure,
        table_calculation: quiz_start_rate, _type_hint: number}, {category: table_calculation,
        expression: "${visitors_view.total_quiz_finishes}/${permanent_session_view.count_distinct_sessions}",
        label: Email Capture Rate, value_format: !!null '', value_format_name: percent_2,
        _kind_hint: measure, table_calculation: email_capture_rate, _type_hint: number}]
    row: 14
    col: 0
    width: 24
    height: 6
  - title: Overall Bottom of Funnel
    name: Overall Bottom of Funnel
    model: testing_model
    explore: permanent_session_view
    type: looker_line
    fields: [user_view.overall_bottom_of_funnel_conversion, permanent_session_view.session_date_month]
    fill_fields: [permanent_session_view.session_date_month]
    filters:
      permanent_session_view.entry_page: "-%blog%"
      permanent_session_view.is_bot: 'No'
      permanent_session_view.session_date_month: 12 months ago for 12 months
    sorts: [permanent_session_view.session_date_month desc]
    limit: 500
    filter_expression: "if(is_null(${user_view.date_joined_time}), now(),\n \
      \ ${user_view.date_joined_time}) > ${permanent_session_view.session_date_week}\
      \ \n\n# Need to make sure they signed up after the session (OR never signed\
      \ up at all) in order for the psession to count"
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
    show_value_labels: true
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    color_application:
      collection_id: 1297ec12-86a5-4ae0-9dfc-82de70b3806a
      palette_id: 93f8aeb4-3f4a-4cd7-8fee-88c3417516a1
      options:
        steps: 5
    series_colors:
      user_view.overall_bottom_of_funnel_conversion: "#FD9577"
    defaults_version: 1
    row: 20
    col: 0
    width: 24
    height: 6
  - name: Quiz Start to Finish Rate
    title: Quiz Start to Finish Rate
    merged_queries:
    - model: testing_model
      explore: permanent_session_view
      type: looker_line
      fields: [permanent_session_view.count_distinct_sessions, permanent_session_view.session_date_month]
      fill_fields: [permanent_session_view.session_date_month]
      filters:
        permanent_session_view.session_date_date: 12 months ago for 12 months
        permanent_session_view.entry_page: "-%blog%"
        permanent_session_view.is_bot: 'No'
      sorts: [permanent_session_view.session_date_month desc]
      limit: 500
      filter_expression: "if(is_null(${user_view.date_joined_time}), now(),\n\
        \  ${user_view.date_joined_time}) > ${permanent_session_view.session_date_week} "
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
      defaults_version: 1
      join_fields: []
    - model: testing_model
      explore: visitors_view
      type: table
      fields: [visitors_view.session_time_month, visitors_view.total_quiz_starts,
        visitors_view.total_quiz_finishes]
      fill_fields: [visitors_view.session_time_month]
      filters:
        visitors_view.session_time_date: 12 months ago for 12 months
        visitors_view.entry_page: "-%blog%"
        visitors_view.is_bot: 'No'
      sorts: [visitors_view.session_time_month desc]
      limit: 500
      query_timezone: America/Los_Angeles
      join_fields:
      - field_name: visitors_view.session_time_month
        source_field_name: permanent_session_view.session_date_month
    color_application:
      collection_id: ed5756e2-1ba8-4233-97d2-d565e309c03b
      palette_id: ff31218a-4f9d-493c-ade2-22266f5934b8
      options:
        steps: 5
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    y_axes: [{label: '', orientation: left, series: [{axisId: permanent_session_view.distinct_sessions,
            id: permanent_session_view.distinct_sessions, name: Distinct Sessions}],
        showLabels: true, showValues: true, unpinAxis: false, tickDensity: default,
        type: linear}, {label: !!null '', orientation: right, series: [{axisId: orders_conversion,
            id: orders_conversion, name: Orders Conversion}], showLabels: true, showValues: true,
        unpinAxis: false, tickDensity: default, type: linear}]
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
    series_types: {}
    point_style: none
    series_colors:
      orders_conversion: "#E52592"
      quiz_finish_rate: "#7CB342"
      quiz_start_to_finish_rate: "#8735C1"
    show_value_labels: true
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    custom_color_enabled: true
    show_single_value_title: true
    single_value_title: Quiz Start Rate
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    hidden_fields: [visitors_view.total_quiz_starts, profiles_orders.count,
      consultationrates.total_quiz_finishes, visitors_view.quiz_finish_rate_by_distinct_sessions,
      visitors_view.quiz_start_rate, user_view.bottom_of_funnel_conversion_within_24_hours,
      permanent_session_view.distinct_sessions, permanent_session_view.count_distinct_sessions,
      visitors_view.total_quiz_finishes, quiz_start_rate, email_capture_rate]
    type: looker_line
    series_column_widths:
      user_view.bottom_of_funnel_conversion_within_24_hours: 143
    sorts: [visitors_view.session_time_week]
    dynamic_fields: [{category: table_calculation, expression: "${visitors_view.total_quiz_starts}\
          \ /${permanent_session_view.count_distinct_sessions}", label: Quiz  Start
          Rate, value_format: !!null '', value_format_name: percent_2, _kind_hint: measure,
        table_calculation: quiz_start_rate, _type_hint: number}, {category: table_calculation,
        expression: "${visitors_view.total_quiz_finishes}/${permanent_session_view.count_distinct_sessions}",
        label: Email Capture Rate, value_format: !!null '', value_format_name: percent_2,
        _kind_hint: measure, table_calculation: email_capture_rate, _type_hint: number},
      {category: table_calculation, expression: "${visitors_view.total_quiz_finishes}/${visitors_view.total_quiz_starts}",
        label: Quiz Start to Finish Rate, value_format: !!null '', value_format_name: percent_2,
        _kind_hint: measure, table_calculation: quiz_start_to_finish_rate, _type_hint: number}]
    row: 7
    col: 0
    width: 24
    height: 7
  - name: Overall Site Conversion - New
    title: Overall Site Conversion - New
    merged_queries:
    - model: testing_model
      explore: permanent_session_view
      type: looker_line
      fields: [permanent_session_view.count_distinct_sessions, permanent_session_view.session_date_month,
        total_converted, count_joined]
      fill_fields: [permanent_session_view.session_date_month]
      filters:
        permanent_session_view.entry_page: "-%blog%"
        permanent_session_view.is_bot: 'No'
        permanent_session_view.session_date_month: 12 months ago for 12 months
      sorts: [permanent_session_view.session_date_month desc]
      limit: 500
      dynamic_fields: [{category: measure, expression: !!null '', label: total converted,
          value_format: !!null '', value_format_name: !!null '', based_on: orders_view.profile_id,
          _kind_hint: measure, measure: total_converted, type: count_distinct, _type_hint: number,
          filters: {user_view.date_joined_date: '2021', permanent_session_view.entry_page: "-%blog%"}},
        {category: table_calculation, expression: "${total_converted}/${count_joined}",
          label: bottom of funnel, value_format: !!null '', value_format_name: percent_2,
          _kind_hint: measure, table_calculation: bottom_of_funnel, _type_hint: number},
        {category: measure, expression: !!null '', label: count joined, value_format: !!null '',
          value_format_name: !!null '', based_on: user_view.id, _kind_hint: measure,
          measure: count_joined, type: count_distinct, _type_hint: number, filters: {
            user_view.date_joined_date: '2021'}}]
      filter_expression: "if(is_null(${user_view.date_joined_time}), now(),\n\
        \  ${user_view.date_joined_time}) > ${permanent_session_view.session_date_week} "
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
      defaults_version: 1
      join_fields: []
    - model: testing_model
      explore: visitors_view
      type: table
      fields: [visitors_view.session_time_month, visitors_view.total_quiz_starts,
        visitors_view.total_quiz_finishes]
      fill_fields: [visitors_view.session_time_month]
      filters:
        visitors_view.session_time_date: 12 months ago for 12 months
        visitors_view.entry_page: "-%blog%"
        visitors_view.is_bot: 'No'
      sorts: [visitors_view.session_time_month desc]
      limit: 500
      query_timezone: America/Los_Angeles
      join_fields:
      - field_name: visitors_view.session_time_month
        source_field_name: permanent_session_view.session_date_month
    color_application:
      collection_id: 7c56cc21-66e4-41c9-81ce-a60e1c3967b2
      palette_id: 5d189dfc-4f46-46f3-822b-bfb0b61777b1
      options:
        steps: 5
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    y_axes: [{label: '', orientation: left, series: [{axisId: permanent_session_view.distinct_sessions,
            id: permanent_session_view.distinct_sessions, name: Distinct Sessions}],
        showLabels: true, showValues: true, unpinAxis: false, tickDensity: default,
        type: linear}, {label: !!null '', orientation: right, series: [{axisId: orders_conversion,
            id: orders_conversion, name: Orders Conversion}], showLabels: true, showValues: true,
        unpinAxis: false, tickDensity: default, type: linear}]
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
    series_types: {}
    point_style: none
    series_colors:
      orders_conversion: "#E52592"
      quiz_finish_rate: "#7CB342"
      overall_site_conversion: "#F9AB00"
    show_value_labels: true
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: linear
    custom_color_enabled: true
    show_single_value_title: true
    single_value_title: Quiz Start Rate
    show_comparison: false
    comparison_type: value
    comparison_reverse_colors: false
    show_comparison_label: true
    enable_conditional_formatting: false
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    hidden_fields: [visitors_view.total_quiz_starts, profiles_orders.count,
      consultationrates.total_quiz_finishes, visitors_view.quiz_finish_rate_by_distinct_sessions,
      visitors_view.quiz_start_rate, user_view.bottom_of_funnel_conversion_within_24_hours,
      permanent_session_view.distinct_sessions, visitors_view.total_quiz_finishes,
      quiz_start_rate, email_capture_rate, bottom_of_funnel, count_joined, total_converted,
      permanent_session_view.count_distinct_sessions]
    type: looker_line
    series_column_widths:
      user_view.bottom_of_funnel_conversion_within_24_hours: 143
    sorts: [visitors_view.session_time_week]
    dynamic_fields: [{category: table_calculation, expression: "${visitors_view.total_quiz_starts}\
          \ /${permanent_session_view.count_distinct_sessions}", label: Quiz  Start
          Rate, value_format: !!null '', value_format_name: percent_2, _kind_hint: measure,
        table_calculation: quiz_start_rate, _type_hint: number}, {category: table_calculation,
        expression: "${visitors_view.total_quiz_finishes}/${permanent_session_view.count_distinct_sessions}",
        label: Email Capture Rate, value_format: !!null '', value_format_name: percent_2,
        _kind_hint: measure, table_calculation: email_capture_rate, _type_hint: number},
      {category: table_calculation, expression: "${bottom_of_funnel}*${email_capture_rate}",
        label: Overall Site Conversion, value_format: !!null '', value_format_name: percent_2,
        _kind_hint: measure, table_calculation: overall_site_conversion, _type_hint: number}]
    row: 26
    col: 0
    width: 24
    height: 6