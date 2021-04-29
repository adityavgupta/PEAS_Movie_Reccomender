DELIMITER ;;
CREATE TRIGGER ImpressionInsert
AFTER INSERT ON Review_movie

FOR EACH ROW
  BEGIN
    SET @score = (SELECT score FROM Review_movie WHERE user_id = new.user_id AND title_id = new.title_id AND type_id = new.type_id);
    SET @movie_exists = (SELECT impression FROM Impressions_M WHERE user_id = new.user_id AND title_id = new.title_id);
    
    IF @movie_exists IS NOT NULL and @score >= 5 then
        UPDATE Impressions_M SET impression = 1 WHERE user_id = new.user_id and title_id = new.title_id;
    ELSEIF @movie_exists IS NOT NULL and @score < 5 then
        UPDATE Impressions_M SET impression = -1 WHERE user_id = new.user_id and title_id = new.title_id;
    ELSEIF @score >= 5 then
        INSERT INTO Impressions_M VALUES(new.title_id, new.user_id, 1);
    ELSE
        INSERT INTO Impressions_M VALUES(new.title_id, new.user_id, -1);
    END IF;
  END;;
  DELIMITER ;