SELECT distinct EXTRACT(year FROM purchased_at) FROM final.carts
where purchased_at IS NOT NULL
order by 1