library(synapser)

synapser::synLogin(authToken = Sys.getenv("SYNAPSE_AUTH_TOKEN"))

# It is easiest to use a fileview to get all nested children in "Samples"
SampleTracking <- "syn52225331"

tb <- synapser::synTableQuery(glue::glue("select id from {SampleTracking}"))
ids <- as.data.frame(tb)$id

asPatientID <- function(s) regmatches(s, regexpr("[A-Z]+[0-9]?-?[0-9]+", s))

errors <- c()

for(i in ids) {
  
  entity <- synapser::synGet(i, downloadFile = FALSE)
  pID <- asPatientID(entity$properties$name)
  entity$annotations$PatientID <- pID
  
  # For now, let's just use the entity name as sample name
  entity$annotations$SampleID <- entity$properties$name
  tryCatch(synapser::synStore(entity), error = function(e) { cat("Skipped ", i, "\n"); errors <- append(errors, i) })
}



