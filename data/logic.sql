
user_controller

find_detail

  - find access_token
    select user_id from Token where id = %id

/*
  select distinct u.id user_id, u.name user_name, g.id group_id, g.name group_name, c.id customer_id, c.name customer_name, r.id role_id, r.name role_name
  from User u
  left join Group_User gu on gu.user_id = u.id
  left join `Group` g on g.id = gu.group_id
  left join Customer c on g.customer_id = c.id
  left join Role r on g.role_id = r.id
  where u.id = (select user_id from Token where id = '%token_id')

  select r.name role_name, f.id function_id, f.name function_name, p.id permission_id, p.res_name resource_name, p.action action
  from Role r
  left join Role_Function rf on rf.role_id = r.id
  left join Function f on rf.function_id = f.id
  left join Function_Permission fp on fp.function_id = f.id
  left join Permission p on fp.permission_id = p.id
  where r.id = '%role_id'
  order by f.id
*/


/**** For Given User ****/

  /* Get user detail with its groups/functions of the given user */
    select u.id user_id, u.name user_name, g.id group_id, g.name group_name,
    c.id customer_id, c.name customer_name, r.id role_id, r.name role_name,
    f.id function_id, f.name function_name, p.id permission_id, p.res_name resource_name, p.action action
    from User u
    left join Group_User gu on gu.user_id = u.id
    left join `Group` g on g.id = gu.group_id
    left join Customer c on g.customer_id = c.id
    left join Role r on g.role_id = r.id
    left join Role_Function rf on rf.role_id = r.id
    left join Function f on rf.function_id = f.id
    left join Function_Permission fp on fp.function_id = f.id
    left join Permission p on fp.permission_id = p.id
    where u.id = (select user_id from Token where id = '%token_id')

/*
  # Using Temporary Table

    create temporary table user_detail as
    	select u.id user_id, u.name user_name, g.id group_id, g.name group_name,
      c.id customer_id, c.name customer_name, r.id role_id, r.name role_name,
      f.id function_id, f.name function_name, p.id permission_id, p.res_name resource_name, p.action action
      from User u
      left join Group_User gu on gu.user_id = u.id
      left join `Group` g on g.id = gu.group_id
      left join Customer c on g.customer_id = c.id
      left join Role r on g.role_id = r.id
      left join Role_Function rf on rf.role_id = r.id
      left join Function f on rf.function_id = f.id
      left join Function_Permission fp on fp.function_id = f.id
      left join Permission p on fp.permission_id = p.id
      where u.id = (select user_id from Token where id = 'c3b39a6b-6323-4803-a136-382a0aa0462e')

    select distinct user_id, user_name, customer_id, customer_name from user_detail

    select distinct group_id, group_name, customer_name, customer_id from user_detail

    select distinct function_id, function_name, permission_id, resource_name, action from user_detail
    order by function_id
*/

  /* Get all groups of given user */
    select c.id customer_id, c.name customer_name, g.id group_id, g.name group_name
    from User u
    left join Group_User gu on gu.user_id = u.id
    left join `Group` g on g.id = gu.group_id
    left join Customer c on g.customer_id = c.id
    where u.id = (select user_id from Token where id = 'c3b39a6b-6323-4803-a136-382a0aa0462e')
    order by c.name, g.name

  /* Get all users of all groups where the given user belongs */
    select c.id customer_id, c.name customer_name, g.id group_id, g.name group_name, u.id user_id, u.name user_name
    from User u
    left join Group_User gu on gu.user_id = u.id
    left join `Group` g on g.id = gu.group_id
    left join Customer c on g.customer_id = c.id
    where g.id in (select group_id from Group_User where user_id = (
      select user_id from Token where id = 'c3b39a6b-6323-4803-a136-382a0aa0462e')
    )
    order by c.name, g.name, u.id


/**** For Customer Admin ****/

  /* Get all functions of the customer where the given user belongs */
    select distinct c.id customer_id, c.name customer_name, g.id group_id, g.name group_name,
    r.id role_id, r.name role_name, f.id function_id, f.name function_name, p.id permission_id,
    p.res_name resource_name, p.action action, p.value val
    from `Group` g
    left join Group_User gu on gu.group_id = g.id
    left join Customer c on g.customer_id = c.id
    left join Role r on g.role_id = r.id
    left join Role_Function rf on rf.role_id = r.id
    left join Function f on rf.function_id = f.id
    left join Function_Permission fp on fp.function_id = f.id
    left join Permission p on fp.permission_id = p.id
    where c.id in (select customer_id from `Group` g
        left join Group_User gu on gu.group_id = g.id
        where gu.user_id = (
          select user_id from Token where id = 'c3b39a6b-6323-4803-a136-382a0aa0462e'
        )
    )
    order by c.name, g.name, r.name, f.name, p.res_name, p.action

    /*
    create temporary table customer_admin as
        select distinct c.id customer_id, c.name customer_name, g.id group_id, g.name group_name,
        r.id role_id, r.name role_name, f.id function_id, f.name function_name, p.id permission_id,
        p.res_name resource_name, p.action action, p.value val
        from `Group` g
        left join Group_User gu on gu.group_id = g.id
        left join Customer c on g.customer_id = c.id
        left join Role r on g.role_id = r.id
        left join Role_Function rf on rf.role_id = r.id
        left join Function f on rf.function_id = f.id
        left join Function_Permission fp on fp.function_id = f.id
        left join Permission p on fp.permission_id = p.id
        where c.id in (select customer_id from `Group` g
            left join Group_User gu on gu.group_id = g.id
            where gu.user_id = (
              select user_id from Token where id = 'c3b39a6b-6323-4803-a136-382a0aa0462e'
            )
        )

    select distinct group_id, group_name from customer_admin order by group_id
    select distinct role_id, role_name, function_id, function_name from customer_admin order by role_id, function_name
    select distinct function_id, function_name, permission_id, resource_name, action from customer_admin order by function_name, resource_name, action

    drop table customer_admin
    */

  /* Get all groups of the customer where the given user belongs */
    select c.id customer_id, c.name customer_name, g.id group_id, g.name group_name
    from `Group` g
    left join Customer c on g.customer_id = c.id
    where c.id in (select customer_id from `Group` g
        left join Group_User gu on gu.group_id = g.id
        where gu.user_id = (
          select user_id from Token where id = 'c3b39a6b-6323-4803-a136-382a0aa0462e'
        )
    )
    order by c.name, g.name

    /*
    select c.id customer_id, c.name customer_name, g.id group_id, g.name group_name
    from `Group` g
    left join Customer c on g.customer_id = c.id
    where c.id = '64b3bbf4-1f3d-446f-b697-06c2a68f2053'
    */

  /* Get all users of the customer where the given user belongs
     This includes the groups without any users */
    select c.id customer_id, c.name customer_name, g.id group_id, g.name group_name, u.id user_id, u.name user_name
    from User u
    left join Group_User gu on gu.user_id = u.id
    right join `Group` g on g.id = gu.group_id
    left join Customer c on g.customer_id = c.id
    where c.id in (select customer_id from `Group` g
        left join Group_User gu on gu.group_id = g.id
        where gu.user_id = (
          select user_id from Token where id = 'c3b39a6b-6323-4803-a136-382a0aa0462e'
        )
    )
    order by c.name, g.name, u.id

    /*
    select c.id customer_id, c.name customer_name, g.id group_id, g.name group_name, u.id user_id, u.name user_name
    from User u
    left join Group_User gu on gu.user_id = u.id
    left join `Group` g on g.id = gu.group_id
    left join Customer c on g.customer_id = c.id
    where c.id = '64b3bbf4-1f3d-446f-b697-06c2a68f2053'
    */
