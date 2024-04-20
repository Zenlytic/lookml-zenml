- dashboard: monthly_kpis_dashboard
  title: Monthly KPIs Dashboard
  layout: newspaper
  preferred_viewer: dashboards-next
  description: ''
  filters:
  - name: Is Test (Yes / No)
    title: Is Test (Yes / No)
    type: field_filter
    default_value: 'No'
    allow_multiple_values: true
    required: false
    ui_config:
      type: button_toggles
      display: inline
    model: testing_model
    explore: user_view
    listens_to_filters: []
    field: user_view.is_test
  elements:
  

  - type: button
    name: button_2541
    rich_content_json: '{"text":"MRR","description":"Deep Dives","newTab":true,"alignment":"center","size":"large","style":"FILLED","color":"#000000","href":"https://google.com"}'
    row: 0
    col: 0
    width: 24
    height: 2
  - title: Total MRR
    name: Total MRR
    model: testing_model
    explore: user_view
    type: looker_column
    fields: [profile_facts_view.first_ship_month, lta_view.utm_medium, profile_facts_view.mrr]
    pivots: [lta_view.utm_medium]
    fill_fields: [profile_facts_view.first_ship_month]
    filters: {}
    sorts: [lta_view.utm_medium, profile_facts_view.first_ship_month desc]
    limit: 500
    column_limit: 50
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: false
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: normal
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: true
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    ordering: none
    show_null_labels: false
    show_totals_labels: true
    show_silhouette: false
    totals_color: "#808080"
    y_axes: [{label: '', orientation: left, series: [{axisId: facebook - lta_view.utm_medium_order___null
              - profile_facts_view.mrr, id: facebook - lta_view.utm_medium_order___null
              - profile_facts_view.mrr, name: Facebook}, {axisId: email
              - 0 - profile_facts_view.mrr, id: email - 0 - profile_facts_view.mrr,
            name: Email}],
        showLabels: false, showValues: false, unpinAxis: false, tickDensity: default,
        tickDensityCustom: 5, type: linear}]
    x_axis_zoom: true
    y_axis_zoom: true
    hidden_pivots: {}
    defaults_version: 1
    listen:
      Months: profile_facts_view.first_ship_month
    row: 2
    col: 0
    width: 12
    height: 8
  - title: New Web Visitors
    name: New Web Visitors
    model: testing_model
    explore: user_view
    type: looker_column
    fields: [lta_view.count, lta_view.utm_medium]
    pivots: [lta_view.utm_medium]
    fill_fields: []
    filters:
      lta_view.utm_content: '-Hello'
      users_view.is_employee: ''
    sorts: [lta_view.utm_medium]
    limit: 500
    column_limit: 50
    dynamic_fields:
    - category: dimension
      description: ''
      label: Attribution
      value_format:
      value_format_name:
      calculation_type: group_by
      dimension: attribution
      args:
      - lta_view.utm_channel
      - - label: Marketing
          filter: Referrals,Unknown,Paid
        - label: Email
          filter: Email
        - label: Affiliate
          filter: Affiliate
      -
      _kind_hint: dimension
      _type_hint: string
    - category: measure
      label: Unique mediums
      based_on: lta_view.utm_medium
      _kind_hint: measure
      measure: utm_medium_1
      type: count_distinct
      _type_hint: number
      filters:
        lta_view.utm_channel: Referrals,Unknown,Paid
    - category: table_calculation
      expression: sum(${lta_view.count})
      label: Pipeline value
      value_format:
      value_format_name: percent_1
      _kind_hint: supermeasure
      table_calculation: pipeline_value
      _type_hint: number
      is_disabled: true
    - category: table_calculation
      expression: |-
        ${lta_view.count:row_total}/offset(${lta_view.count:row_total},1)
        -1
      label: Total MoM
      value_format:
      value_format_name: percent_1
      _kind_hint: supermeasure
      table_calculation: total_mom
      _type_hint: number
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: false
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: normal
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: true
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    ordering: none
    show_null_labels: false
    show_totals_labels: true
    show_silhouette: false
    totals_color: "#808080"
    y_axes: []
    x_axis_zoom: true
    y_axis_zoom: true
    series_types:
      number_of_unique_companies: line
    series_colors:
      number_of_contacts: "#808080"
      number_of_unique_companies: "#808080"
    series_labels:
      Facebook Campaign - lta_view.count: Facebook Campaign
      Direct - lta_view.count: Direct
      Email Marketing - lta_view.count: Email Marketing
      Offline - lta_view.count: Offline
      Organic Search - lta_view.count: Organic Search
    show_null_points: true
    interpolation: linear
    defaults_version: 1
    hidden_pivots: {}
    hidden_fields: []
    row: 63
    col: 0
    width: 12
    height: 8
  - name: ''
    type: text
    title_text: ''
    subtitle_text: ''
    body_text: |-
      <font color="MidnightBlue" size="5">
      <center>

      MRR Movements

      </center>
      </font>
    row: 58
    col: 0
    width: 24
    height: 2