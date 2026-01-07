rule Phishing_Login_Form
{
    strings:
        $pw1 = /type\s*=\s*["']password["']/ nocase
        $pw2 = /name\s*=\s*["']password["']/ nocase
        $auth = /(signin|login|verify|account|secure)/ nocase
    condition:
        any of them
}

rule Phishing_JS_Credential_Theft
{
    strings:
        $xhr = /XMLHttpRequest|fetch\(/ nocase
        $post = /method\s*:\s*["']POST["']/ nocase
        $send = /password|credential|auth/ nocase
    condition:
        $xhr and $send
}

rule Phishing_Obfuscated_JS
{
    strings:
        $eval = /eval\(|atob\(|fromCharCode/ nocase
    condition:
        any of them
}
