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