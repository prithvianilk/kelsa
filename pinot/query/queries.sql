select count (1), application, tab from work
where done_at >= 1751667973480
group by 2, 3
order by 1 desc;
