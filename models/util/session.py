def add_and_refresh(session, obj):
    """
    Adds obj to session, commits and refreshes

    Useful when creating new rows and then needing
    the id (that comes from sequence)
    """

    session.add(obj)
    session.commit()
    session.flush()
    session.refresh(obj)
