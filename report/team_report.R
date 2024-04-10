library(synr)
library(httr2)

# There are two projects where access really matters: Breast and Ovarian
# The final idea is to have a report page with 2 sections:
# A. Teams have been added for each of those projects, so Sage governance/Atlas leads can review the institutional teams 
# (Sage governance cares more about/only has the ability for checking at the institutional level, e.g. 
# we can say "the Aparicio team shouldn't be added here", 
# but we cannot say "this person in this team shouldn't be added here" -- that's deferred to the PI/Lab Manager). 
# B. People on those teams, so the PI/Lab Manager can review their specific team membership.
library(synr)

api <- TeamServicesApi$new()
api$api_client$bearer_token <- Sys.getenv("SYNAPSE_AUTH_TOKEN")

test <- api_client$postRepoV1TeamIdMemberListWithHttpInfo(id = 423657)

# We actually implement Section B first as that is the more important part, 
# hard-coding teams that we plan to add to those projects for Phase II.

# Should use the actual team names on Synapse, but Sorger team has confusing/misleading name
teams <- c(
  Brugge = 3423657,
  Drapkin = 3427329,
  Aparicio = 3466987,
  Long = 3466748,
  Ellisen = 3442703,
  Nathanson = 3444501,
  Velculescu = 3444504,
  Eng = 3444502,
  Sung = 0,
  Sorger = 3443961,
  DCC = 3416772,
)

# Part B

get_team_members <- ""
for (team in teams) {
  
}
