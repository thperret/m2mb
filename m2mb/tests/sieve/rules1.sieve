require "fileinto";

if header :contains "Subject" ["private"] {
    fileinto "private";
    stop;
} else {
    if address :contains "To" "user1" {
        redirect "user1";
    } elsif address :contains "To" "user2" {
        redirect "@user2";
    }
}
