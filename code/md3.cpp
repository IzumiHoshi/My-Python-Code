#include "StdAfx.h"
#include ".\md5.h"

void byteReverse(unsigned char *buf, unsigned longs)
{
	unsigned int t;
	do {
		t = (unsigned int) ((unsigned) buf[3] << 8 | buf[2]) << 16 |
			((unsigned) buf[1] << 8 | buf[0]);
		*(unsigned int *) buf = t;
		buf += 4;
	} while (--longs);
}

void MD5_Init(MD5_CONTEXT *ctx)
{
	ctx->buf[0] = 0x67452301;
	ctx->buf[1] = 0xefcdab89;
	ctx->buf[2] = 0x98badcfe;
	ctx->buf[3] = 0x10325476;

	ctx->bits[0] = 0;
	ctx->bits[1] = 0;
}

void MD5_Update( MD5_CONTEXT *ctx, const char *buf, unsigned len)
{
	unsigned int t;

	/* Update bitcount */

	t = ctx->bits[0];
	if ((ctx->bits[0] = t + ((unsigned int) len << 3)) < t)
		ctx->bits[1]++;		/* Carry from low to high */
	ctx->bits[1] += len >> 29;

	t = (t >> 3) & 0x3f;	/* Bytes already in shsInfo->data */

	/* Handle any leading odd-sized chunks */

	if (t) {
		unsigned char *p = (unsigned char *) ctx->in + t;

		t = 64 - t;
		if (len < t) {
			memcpy(p, buf, len);
			return;
		}
		memcpy(p, buf, t);
		byteReverse(ctx->in, 16);
		MD5Transform(ctx->buf, (unsigned int *) ctx->in);
		buf += t;
		len -= t;
	}
	/* Process data in 64-byte chunks */

	while (len >= 64) {
		memcpy(ctx->in, buf, 64);
		byteReverse(ctx->in, 16);
		MD5Transform(ctx->buf, (unsigned int *) ctx->in);
		buf += 64;
		len -= 64;
	}

	/* Handle any remaining bytes of data. */

	memcpy(ctx->in, buf, len);
}

void MD5_Final(MD5_CONTEXT *ctx, char digest[16])
{
	unsigned count;
	unsigned char *p;

	/* Compute number of bytes mod 64 */
	count = (ctx->bits[0] >> 3) & 0x3F;

	/* Set the first char of padding to 0x80.  This is safe since there is
	always at least one byte free */
	p = ctx->in + count;
	*p++ = 0x80;

	/* Bytes of padding needed to make 64 bytes */
	count = 64 - 1 - count;

	/* Pad out to 56 mod 64 */
	if (count < 8) {
		/* Two lots of padding:  Pad the first block to 64 bytes */
		memset(p, 0, count);
		byteReverse(ctx->in, 16);
		MD5Transform(ctx->buf, (unsigned int *) ctx->in);

		/* Now fill the next block with 56 bytes */
		memset(ctx->in, 0, 56);
	} else {
		/* Pad block to 56 bytes */
		memset(p, 0, count - 8);
	}
	byteReverse(ctx->in, 14);

	/* Append length in bits and transform */
	((unsigned int *) ctx->in)[14] = ctx->bits[0];
	((unsigned int *) ctx->in)[15] = ctx->bits[1];

	MD5Transform(ctx->buf, (unsigned int *) ctx->in);
	byteReverse((unsigned char *) ctx->buf, 4);
	memcpy(digest, ctx->buf, 16);
	memset(ctx, 0, sizeof(ctx));	/* In case it's sensitive */
}

void MD5Transform(unsigned int buf[4], unsigned int const in[16])
{
	register unsigned int a, b, c, d;

	a = buf[0];
	b = buf[1];
	c = buf[2];
	d = buf[3];

	MD5STEP(F1, a, b, c, d, in[0] + 0xd76aa478, 7);
	MD5STEP(F1, d, a, b, c, in[1] + 0xe8c7b756, 12);
	MD5STEP(F1, c, d, a, b, in[2] + 0x242070db, 17);
	MD5STEP(F1, b, c, d, a, in[3] + 0xc1bdceee, 22);
	MD5STEP(F1, a, b, c, d, in[4] + 0xf57c0faf, 7);
	MD5STEP(F1, d, a, b, c, in[5] + 0x4787c62a, 12);
	MD5STEP(F1, c, d, a, b, in[6] + 0xa8304613, 17);
	MD5STEP(F1, b, c, d, a, in[7] + 0xfd469501, 22);
	MD5STEP(F1, a, b, c, d, in[8] + 0x698098d8, 7);
	MD5STEP(F1, d, a, b, c, in[9] + 0x8b44f7af, 12);
	MD5STEP(F1, c, d, a, b, in[10] + 0xffff5bb1, 17);
	MD5STEP(F1, b, c, d, a, in[11] + 0x895cd7be, 22);
	MD5STEP(F1, a, b, c, d, in[12] + 0x6b901122, 7);
	MD5STEP(F1, d, a, b, c, in[13] + 0xfd987193, 12);
	MD5STEP(F1, c, d, a, b, in[14] + 0xa679438e, 17);
	MD5STEP(F1, b, c, d, a, in[15] + 0x49b40821, 22);

	MD5STEP(F2, a, b, c, d, in[1] + 0xf61e2562, 5);
	MD5STEP(F2, d, a, b, c, in[6] + 0xc040b340, 9);
	MD5STEP(F2, c, d, a, b, in[11] + 0x265e5a51, 14);
	MD5STEP(F2, b, c, d, a, in[0] + 0xe9b6c7aa, 20);
	MD5STEP(F2, a, b, c, d, in[5] + 0xd62f105d, 5);
	MD5STEP(F2, d, a, b, c, in[10] + 0x02441453, 9);
	MD5STEP(F2, c, d, a, b, in[15] + 0xd8a1e681, 14);
	MD5STEP(F2, b, c, d, a, in[4] + 0xe7d3fbc8, 20);
	MD5STEP(F2, a, b, c, d, in[9] + 0x21e1cde6, 5);
	MD5STEP(F2, d, a, b, c, in[14] + 0xc33707d6, 9);
	MD5STEP(F2, c, d, a, b, in[3] + 0xf4d50d87, 14);
	MD5STEP(F2, b, c, d, a, in[8] + 0x455a14ed, 20);
	MD5STEP(F2, a, b, c, d, in[13] + 0xa9e3e905, 5);
	MD5STEP(F2, d, a, b, c, in[2] + 0xfcefa3f8, 9);
	MD5STEP(F2, c, d, a, b, in[7] + 0x676f02d9, 14);
	MD5STEP(F2, b, c, d, a, in[12] + 0x8d2a4c8a, 20);

	MD5STEP(F3, a, b, c, d, in[5] + 0xfffa3942, 4);
	MD5STEP(F3, d, a, b, c, in[8] + 0x8771f681, 11);
	MD5STEP(F3, c, d, a, b, in[11] + 0x6d9d6122, 16);
	MD5STEP(F3, b, c, d, a, in[14] + 0xfde5380c, 23);
	MD5STEP(F3, a, b, c, d, in[1] + 0xa4beea44, 4);
	MD5STEP(F3, d, a, b, c, in[4] + 0x4bdecfa9, 11);
	MD5STEP(F3, c, d, a, b, in[7] + 0xf6bb4b60, 16);
	MD5STEP(F3, b, c, d, a, in[10] + 0xbebfbc70, 23);
	MD5STEP(F3, a, b, c, d, in[13] + 0x289b7ec6, 4);
	MD5STEP(F3, d, a, b, c, in[0] + 0xeaa127fa, 11);
	MD5STEP(F3, c, d, a, b, in[3] + 0xd4ef3085, 16);
	MD5STEP(F3, b, c, d, a, in[6] + 0x04881d05, 23);
	MD5STEP(F3, a, b, c, d, in[9] + 0xd9d4d039, 4);
	MD5STEP(F3, d, a, b, c, in[12] + 0xe6db99e5, 11);
	MD5STEP(F3, c, d, a, b, in[15] + 0x1fa27cf8, 16);
	MD5STEP(F3, b, c, d, a, in[2] + 0xc4ac5665, 23);

	MD5STEP(F4, a, b, c, d, in[0] + 0xf4292244, 6);
	MD5STEP(F4, d, a, b, c, in[7] + 0x432aff97, 10);
	MD5STEP(F4, c, d, a, b, in[14] + 0xab9423a7, 15);
	MD5STEP(F4, b, c, d, a, in[5] + 0xfc93a039, 21);
	MD5STEP(F4, a, b, c, d, in[12] + 0x655b59c3, 6);
	MD5STEP(F4, d, a, b, c, in[3] + 0x8f0ccc92, 10);
	MD5STEP(F4, c, d, a, b, in[10] + 0xffeff47d, 15);
	MD5STEP(F4, b, c, d, a, in[1] + 0x85845dd1, 21);
	MD5STEP(F4, a, b, c, d, in[8] + 0x6fa87e4f, 6);
	MD5STEP(F4, d, a, b, c, in[15] + 0xfe2ce6e0, 10);
	MD5STEP(F4, c, d, a, b, in[6] + 0xa3014314, 15);
	MD5STEP(F4, b, c, d, a, in[13] + 0x4e0811a1, 21);
	MD5STEP(F4, a, b, c, d, in[4] + 0xf7537e82, 6);
	MD5STEP(F4, d, a, b, c, in[11] + 0xbd3af235, 10);
	MD5STEP(F4, c, d, a, b, in[2] + 0x2ad7d2bb, 15);
	MD5STEP(F4, b, c, d, a, in[9] + 0xeb86d391, 21);

	buf[0] += a;
	buf[1] += b;
	buf[2] += c;
	buf[3] += d;
}

void CvtHex( IN HASH Bin,
	OUT HASHHEX Hex)
{
	unsigned short i;
	unsigned char j;
	for (i = 0; i < HASHLEN; i++)
	{
		j = (Bin[i] >> 4) & 0xf;
		if (j <= 9) Hex[i*2] = (j + '0');
		else Hex[i*2] = (j + 'a' - 10);
		j = Bin[i] & 0xf;
		if (j <= 9) Hex[i*2+1] = (j + '0');
		else Hex[i*2+1] = (j + 'a' - 10);
	};
	Hex[HASHHEXLEN] = '\0';
};

void DigestCalcHA1( IN INT8 * pszAlg, IN INT8 * pszUserName, IN INT8 * pszRealm,
                    IN INT8 * pszPassword, IN INT8 * pszNonce,
                    IN INT8 * pszCNonce, OUT HASHHEX SessionKey)
{
    MD5_CONTEXT 	Md5Ctx;
    HASH 		HA1;

    MD5_Init(&Md5Ctx);
    MD5_Update(&Md5Ctx, (char*)pszUserName, strlen((char*)pszUserName));
    MD5_Update(&Md5Ctx, ":", 1);
    MD5_Update(&Md5Ctx, (char*)pszRealm, strlen((char*)pszRealm));
    MD5_Update(&Md5Ctx, ":", 1);
    MD5_Update(&Md5Ctx, (char*)pszPassword, strlen((char*)pszPassword));
    MD5_Final(&Md5Ctx, HA1);
    if (strcmp((char*)pszAlg, "md5-sess") == 0)
    {
        MD5_Init(&Md5Ctx);
        MD5_Update(&Md5Ctx, HA1, HASHLEN);
        MD5_Update(&Md5Ctx, ":", 1);
        MD5_Update(&Md5Ctx, (char*)pszNonce, strlen((char*)pszNonce));
        MD5_Update(&Md5Ctx, ":", 1);
        MD5_Update(&Md5Ctx, (char*)pszCNonce, strlen((char*)pszCNonce));
        MD5_Final(&Md5Ctx, HA1);
    };
    CvtHex(HA1, SessionKey);
}
/*******************************************************************************
 * Function:    DigestCalcResponse 
 *
 * Description: calculate request-digest/response-digest as per HTTP Digest spec
 *
 * Parameters :
 *      [IN]    HASHHEX HA1 		- Hex value of HA1
 *      [IN]    INT8 * pszNonce		- Nonce value 
 *      [IN]    INT8 * pszNonceCount- Count of nonce 
 *      [IN]    INT8 * pszCNonce	- Cnonce value 
 *      [IN]    INT8 * pszQop		- Qop value 
 *      [IN]    INT8 * pszMethod	- Method name 
 *      [IN]    INT8 * pszDigestUri - Digest URI
 *      [IN]    HASHHEX HEntity		- HEntity
 *      [OUT]   HASHHEX Response	- Response 
 *
 * Return Value: NONE
 ******************************************************************************/
void DigestCalcResponse(IN HASHHEX HA1, IN INT8 * pszNonce, 
                        IN INT8 * pszNonceCount, IN INT8 * pszCNonce,
                        IN INT8 * pszQop, IN INT8 * pszMethod,
                        IN INT8 * pszDigestUri, IN HASHHEX HEntity,
                        OUT HASHHEX Response)
{
      //MD5_CONTEXT Md5Ctx;
      //HASH HA2;
      //HASH RespHash;
      //HASHHEX HA2Hex;

      ///* calculate H(A2)													  */
      //MD5_Init(&Md5Ctx);
      //MD5_Update(&Md5Ctx, (char*)pszMethod, strlen((char*)pszMethod));
      //MD5_Update(&Md5Ctx, ":", 1);
      //MD5_Update(&Md5Ctx, (char*)pszDigestUri, strlen((char*)pszDigestUri));
      //if(pszQop == NULL)
      ////if (strcmp((char*)pszQop, "auth-int") == 0) {		
      ////      MD5_Update(&Md5Ctx, ":", 1);
      ////      MD5_Update(&Md5Ctx, HEntity, HASHHEXLEN);
      ////};
      //MD5_Final(&Md5Ctx, HA2);
      //CvtHex(HA2, HA2Hex);

      ///* calculate response													  */
      //MD5_Init(&Md5Ctx);
      //MD5_Update(&Md5Ctx, HA1, HASHHEXLEN);
      //MD5_Update(&Md5Ctx, ":", 1);
      //MD5_Update(&Md5Ctx, (char*)pszNonce, strlen((char*)pszNonce));
      //MD5_Update(&Md5Ctx, ":", 1);
      //if (pszQop != NULL) {	  
      //    MD5_Update(&Md5Ctx, (char*)pszNonceCount, strlen((char*)pszNonceCount));
      //    MD5_Update(&Md5Ctx, ":", 1);
      //    MD5_Update(&Md5Ctx, (char*)pszCNonce, strlen((char*)pszCNonce));
      //    MD5_Update(&Md5Ctx, ":", 1);
      //    MD5_Update(&Md5Ctx, (char*)pszQop, strlen((char*)pszQop));
      //    MD5_Update(&Md5Ctx, ":", 1);
      //};
      //MD5_Update(&Md5Ctx, HA2Hex, HASHHEXLEN);
      //MD5_Final(&Md5Ctx, RespHash);
      //CvtHex(RespHash, Response);
	int Aka = 0;

	MD5_CONTEXT Md5Ctx;
	HASH HA2;
	HASH RespHash;
	HASHHEX HA2Hex;

	/* calculate H(A2) */
	MD5_Init(&Md5Ctx);
	MD5_Update(&Md5Ctx, (char *)pszMethod, strlen((char*)pszMethod));
	MD5_Update(&Md5Ctx, ":", 1);
	MD5_Update(&Md5Ctx, (char *)pszDigestUri, strlen((char*)pszDigestUri));

	if (pszQop == NULL) {
		goto auth_withoutqop;
	} else if (0 == stricmp((char *)pszQop, "auth-int")) {
		goto auth_withauth_int;
	} else if (0 == stricmp((char *)pszQop, "auth")) {
		goto auth_withauth;
	}

auth_withoutqop:
	MD5_Final(&Md5Ctx, HA2);
	CvtHex(HA2, HA2Hex);

	/* calculate response */
	MD5_Init(&Md5Ctx);
	MD5_Update(&Md5Ctx, (char *) HA1, HASHHEXLEN);
	MD5_Update(&Md5Ctx, (char *) ":", 1);
	MD5_Update(&Md5Ctx, (char *) pszNonce, strlen((char *)pszNonce));
	MD5_Update(&Md5Ctx, (char *) ":", 1);

	goto end;

auth_withauth_int:

	MD5_Update(&Md5Ctx, (char *) ":", 1);
	MD5_Update(&Md5Ctx, (char *) HEntity, HASHHEXLEN);

auth_withauth:
	MD5_Final(&Md5Ctx, HA2);
	CvtHex(HA2, HA2Hex);

	/* calculate response */
	MD5_Init(&Md5Ctx);
	MD5_Update(&Md5Ctx, (char *) HA1, HASHHEXLEN);
	MD5_Update(&Md5Ctx, (char *) ":", 1);
	MD5_Update(&Md5Ctx, (char *) pszNonce, strlen((char *)pszNonce));
	MD5_Update(&Md5Ctx, (char *) ":", 1);
	if (Aka == 0) {
		MD5_Update(&Md5Ctx, (char *) pszNonceCount,
			strlen((char *)pszNonceCount));
		MD5_Update(&Md5Ctx, (char *) ":", 1);
		MD5_Update(&Md5Ctx, (char *) pszCNonce, strlen((char *)pszCNonce));
		MD5_Update(&Md5Ctx, (char *) ":", 1);
		MD5_Update(&Md5Ctx, (char *) pszQop, strlen((char *)pszQop));
		MD5_Update(&Md5Ctx, (char *) ":", 1);
	}
end:
	MD5_Update(&Md5Ctx, (char *) HA2Hex, HASHHEXLEN);
	MD5_Final(&Md5Ctx, RespHash);
	CvtHex(RespHash, Response);
}

void str_dequote(char *s)
{
	if (s == NULL)
	{
		return;
	}
	
	size_t len;

	if (*s == '\0')
		return;
	if (*s != '"')
		return;
	len = strlen(s);
	memmove(s, s + 1, len--);
	if (len > 0 && s[len - 1] == '"')
		s[--len] = '\0';
	for (; *s != '\0'; s++, len--) {
		if (*s == '\\')
			memmove(s, s + 1, len--);
	}
}