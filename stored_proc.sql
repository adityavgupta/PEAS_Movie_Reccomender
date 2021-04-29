CREATE DEFINER=`root`@`34.121.68.223` PROCEDURE `get_suggested`(IN t_id VARCHAR(20))
BEGIN    
    declare n VARCHAR(500);
    declare ty_id VARCHAR(50);
    declare pop INT;
    declare avg_rat FLOAT;
    declare avail_on VARCHAR(50);
    declare genr VARCHAR(500);
    
    declare n1 VARCHAR(500);
    declare ty_id1 VARCHAR(50);
    declare pop1 INT;
    declare avg_rat1 FLOAT;
    declare avail_on1 VARCHAR(50);
    declare genr1 VARCHAR(500);
    
    declare n2 VARCHAR(500);
    declare ty_id2 VARCHAR(50);
    declare pop2 INT;
    declare avg_rat2 FLOAT;
    declare avail_on2 VARCHAR(50);
    declare genr2 VARCHAR(500);
    declare exit_loop boolean default FALSE;
    
    DECLARE counter INT DEFAULT 1;
    DECLARE counter1 INT;
    DECLARE counter_tmp1 INT DEFAULT 1;
    DECLARE counter2 INT DEFAULT 1;
    DECLARE counter_tmp2 INT DEFAULT 1;
    
    declare cur2 cursor for(select movie.name, movie.type_id, movie.popularity, movie.avg_rating, movie.available_on, movie.genres 
							from movie join Review_movie on movie.title_id = Review_movie.title_id 
                            where release_year = (select release_year from movie where title_id = t_id)
                            group by movie.title_id 
                            order by avg(Review_movie.score) 
                            limit 10);
--     
    declare cur3 cursor for(select movie.name, movie.type_id, movie.popularity, movie.avg_rating, movie.available_on, movie.genres 
 							from movie join Impressions_M on movie.title_id = Impressions_M.title_id
							where movie.avg_rating = (select max(movie.avg_rating) from movie where available_on = (select available_on from movie where title_id = t_id))
							group by movie.title_id
							having count(Impressions_M.impression) > 100
							limit 10);

-- where genres = (select genres from movie where title_id = t_id)
    declare cur1 cursor for((select movie.name, movie.type_id, movie.popularity, movie.avg_rating, movie.available_on, movie.genres from movie where genres = (select genres from movie where title_id = t_id))
							union
							(select movie.name, movie.type_id, movie.popularity, movie.avg_rating, movie.available_on, movie.genres
                            from movie
							where movie.popularity > 8 and genres = (select genres from movie where title_id = t_id)));

    declare continue handler for not found set exit_loop = TRUE;
    SET counter1 = (select count(*) from (select movie.name, movie.type_id, movie.popularity, movie.avg_rating, movie.available_on, movie.genres 
 							from movie join Impressions_M on movie.title_id = Impressions_M.title_id
							where movie.avg_rating = (select max(movie.avg_rating) from movie where available_on = (select available_on from movie where title_id = t_id))
							group by movie.title_id
							having count(Impressions_M.impression) > 100
							limit 10) as Tmp);
                            
	SET counter2 = (select count(*) from (select movie.name, movie.type_id, movie.popularity, movie.avg_rating, movie.available_on, movie.genres 
 							from movie join Impressions_M on movie.title_id = Impressions_M.title_id
							where movie.avg_rating = (select max(movie.avg_rating) from movie where available_on = (select available_on from movie where title_id = t_id))
							group by movie.title_id
							having count(Impressions_M.impression) > 100
							limit 10) as Tmp2);
    
    drop table if exists suggested;
    create table suggested(movie_name varchar(500), type_id varchar(10), popularity int, avg_rating float, available_on varchar(25), genres varchar(500));

     open cur1;
        repeat
            fetch cur1 into n, ty_id, pop, avg_rat, avail_on, genr;
            insert into suggested values(n, ty_id, pop, avg_rat, avail_on, genr);
            set counter = counter + 1;
        until counter >= 50
        end repeat;
    close cur1;

     open cur2;
        repeat
            fetch cur2 into n1, ty_id1, pop1, avg_rat1, avail_on1, genr1;
            insert into suggested values(n1, ty_id1, pop1, avg_rat1, avail_on1, genr1);
            set counter_tmp1 = counter_tmp1 + 1;
        until counter_tmp1 >= counter1
        end repeat;
    close cur2;

     open cur3;
        repeat
            fetch cur3 into n2, ty_id2, pop1, avg_rat2, avail_on2, genr2;
            insert into suggested values(n2, ty_id2, pop2, avg_rat2, avail_on2, genr2);
            set counter_tmp2 = counter_tmp2 + 1;
        until counter_tmp2 >= counter2
        end repeat;
    close cur3;
    
    select * from suggested limit 1;
    
END