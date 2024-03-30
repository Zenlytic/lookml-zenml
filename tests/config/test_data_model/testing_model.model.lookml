connection: "testing-snowflake"

include: "/dashboards/*.dashboard.lookml"

include: "/views/*.view.lkml"
               
datagroup: pdt_refresh_24_hours {
  sql_trigger: select current_date() ;;
  max_cache_age: "24 hours"
}

access_grant: test_access_grant {
  user_attribute: user_attribute_name
  allowed_values: ["value_1", "value_2"]
}

############################ USERS #########################################

explore: user_view {
  label: "Signed in Users"

  join: profile_facts_view {
    view_label: "Profile Facts"
    type: left_outer
    relationship: one_to_one
    sql_on: ${user_view.id} = ${profile_facts_view.profile_id} ;;
  }

  join: orders_view {
    view_label: "Orders"
    type: left_outer
    relationship: one_to_many
    sql_on: ${user_view.id} = ${orders_view.profile_id} ;;
  }

  join: lta_view {
    from: last_touch_attribution_view
    view_label: "Last Touch Attribution"
    type: left_outer
    relationship: many_to_one
    sql_on: ${lta_view.profile_id} = ${orders_view.profile_id}  ;;
  }


  join: marketing_spend_daily {
      view_label: "Marketing Spend (Aligned on OrderWeek)"
      type: left_outer
      relationship: one_to_many
      sql_on: ${marketing_spend_daily.date_date} = ${orders_view.orderdatetime_date};;
  }

}

############################ SESSIONS #########################################


explore: all_visitors_view {
  from:  all_visitors
  label: "Sessions"
  view_label: "All Visitors"

  join: orders_view {
    view_label: "Orders"
    type: left_outer
    sql_on: ${user_view.id} = ${orders_view.profile_id}  ;;
    relationship: one_to_many
  }

  join: session_to_profile_view {
    view_label: "Session to Profile"
    from: session_to_profile
    type: left_outer
    sql_on:  ${all_visitors_view.session_id} = ${session_to_profile_view.session} ;;
    relationship: one_to_one
  }

  join: user_view {
    view_label: "User"
    type: left_outer
    sql_on: ${session_to_profile_view.user_id} = ${user_view.id} ;;
    relationship: many_to_one
  }

  join: profile_facts_view {
    view_label: "Profile Facts"
    type: left_outer
    relationship: one_to_one
    sql_on: ${user_view.id} = ${profile_facts_view.profile_id} ;;
  }

}


############################ ZENDESK #########################################

explore: zendesk_tickets {
  label: "Zendesk"
  join: user_view {
    view_label: "User"
    type: left_outer
    sql_on: ${zendesk_users.email} =${user_view.email} ;;
    relationship: one_to_one
  }

  join: orders_view {
    view_label: "Orders"
    type: left_outer
    sql_on: ${user_view.id} = ${orders_view.profile_id} ;;
    relationship: one_to_many
    fields: [orders_view.id, orders_view.profile_id, orders_view.orderdatetime_date, orders_view.orderdatetime_raw, orders_view.orderdatetime_week, orders_view.orderdatetime_month, orders_view.order_count, orders_view.first_order, orders_view.latest_order]
  }

  join: zendesk_users {
    type: left_outer
    relationship: one_to_one
    sql_on: ${zendesk_tickets.requester_id}=  ${zendesk_users.user_id};;
  }

}
