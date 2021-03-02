CREATE FUNCTION is_valid_json(text)
    RETURNS boolean
    LANGUAGE plpgsql
    IMMUTABLE
    AS $$
    BEGIN
        RETURN CASE WHEN $1::json IS NULL THEN false ELSE true
    END;
    exception 
        WHEN others THEN RETURN FALSE;
    END;
    $$;