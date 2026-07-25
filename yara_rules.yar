rule IRC_Worm_CeUniCo
{
    meta:
        description = "Detects CeUniCo IRC worm batch script"
        author = "Tirodhana"
        severity = "high"
    strings:
        $s1 = "CeUniCo" nocase
        $s2 = "CapsLock" nocase
        $s3 = "dcc send" nocase
        $s4 = "SpeedUp" nocase
    condition:
        2 of them
}

rule Suspicious_Batch_Attrib
{
    meta:
        description = "Detects hidden file attribute abuse"
        severity = "medium"
    strings:
        $a1 = "Attrib +H" nocase
        $a2 = "Attrib +S" nocase
        $a3 = "Attrib +R" nocase
    condition:
        2 of them
}

rule Malicious_File_Spreading
{
    meta:
        description = "Detects file copying to system directories"
        severity = "high"
    strings:
        $f1 = "C:\\Windows\\System32" nocase
        $f2 = "C:\\Windows\\System\\" nocase
        $f3 = "mirc.exe" nocase
        $f4 = "script.ini" nocase
    condition:
        2 of them
}

rule Directory_Enumeration
{
    meta:
        description = "Detects recursive directory listing"
        severity = "low"
    strings:
        $d1 = "Dir /S" nocase
    condition:
        $d1
}
