with user_course as
(
SELECT
    ca.user_id,
    ci.resource_id,
    ca.promo_code_id,
    ca.state
FROM final.cart_items ci
    JOIN final.carts ca ON ci.cart_id = ca.id
    where ci.resource_type = 'Course'
order by 1,2
),

-- Количество клиентов купивших курсы
/*
select count(distinct user_id)
    from user_course
    where state = 'successful'
*/

-- Количество курсов
/*
select count(distinct resource_id)
    from user_course
*/
user_count_course as
(select
    user_id,
    COUNT(distinct resource_id) count_course
  FROM user_course
    where state = 'successful'
group by 1)

select AVG(count_course) from user_count_course

SELECT count(user_id)
    from user_count_course
    where count_course > 1