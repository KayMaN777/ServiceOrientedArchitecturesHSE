CREATE TABLE IF NOT EXISTS Likes (
    userId UInt32,
    postId UInt32,
    updatedAt DateTime,
    PRIMARY KEY (userId, postId)
) ENGINE = MergeTree()
ORDER BY (userId, postId);

CREATE TABLE IF NOT EXISTS Views (
    userId UInt32,
    postId UInt32,
    updatedAt DateTime,
    PRIMARY KEY (userId, postId)
) ENGINE = MergeTree()
ORDER BY (userId, postId);
