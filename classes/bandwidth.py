from datetime import datetime
class bandwidth(object):
    documentId = ""
    bandwidthId = ""
    hostId = ""
    included = ""
    organizationId = ""
    riskScore = ""
    time = datetime.now()
    usage = ""
    process = False;

    def __init__(self, documentId,  bandwidthId, hostId , included, organizationId , riskScore , time , usage , process):
        self.documentId = documentId
        self.bandwidthId = bandwidthId
        self.hostId = hostId;
        self.included = included;
        self.organizationId = organizationId;
        self.riskScore = riskScore;
        self.time = time;
        self.usage = usage;
        self.processed = process;

