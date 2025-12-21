/**
 * Cloudflare Function - detay.asp Query String Redirects
 * Handles old backlink URLs with query parameters
 */

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const params = url.searchParams;

  // Badem - flowers=654 & cicekler=91 (any order)
  if ((params.get('flowers') === '654' && params.get('cicekler') === '91') ||
      (params.get('cicekler') === '91' && params.get('flowers') === '654')) {
    return Response.redirect('https://cicekansiklopedisi.com/bitki/badem/', 301);
  }

  // Limon - Only if it's the cicekler=91&flowers=654 variation without other params
  // (already handled above, but keeping for clarity)

  // Lale - cicekler=67 & flowers=167 & cicek=LALE
  if (params.get('cicekler') === '67' && params.get('flowers') === '167') {
    return Response.redirect('https://cicekansiklopedisi.com/cicek/lale/', 301);
  }

  // Default fallback - redirect to homepage for any other detay.asp requests
  return Response.redirect('https://cicekansiklopedisi.com/', 301);
}
