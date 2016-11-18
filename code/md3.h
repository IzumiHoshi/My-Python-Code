#pragma once
typedef struct tagMD5_CONTEXT
{
	unsigned int buf[4];	/**< buf    */
	unsigned int bits[2];	/**< bits   */
	unsigned char  in[64];	/**< in	    */
}MD5_CONTEXT;

#define F1(x, y, z) (z ^ (x & (y ^ z)))
#define F2(x, y, z) F1(z, x, y)
#define F3(x, y, z) (x ^ y ^ z)
#define F4(x, y, z) (y ^ (x | ~z))

#define MD5STEP(f, w, x, y, z, data, s) \
	( w += f(x, y, z) + data,  w = w<<s | w>>(32-s),  w += x )

#define HASHLEN 16
typedef char HASH[HASHLEN];
#define HASHHEXLEN 32
typedef char HASHHEX[HASHHEXLEN+1];
#define IN
#define OUT

//MD5加密
void MD5Transform(unsigned int buf[4], unsigned int const in[16]);
void MD5_Init(MD5_CONTEXT *pms);
void MD5_Update( MD5_CONTEXT *pms, const char *data, unsigned nbytes);
void MD5_Final(MD5_CONTEXT *pms, char digest[16]);

//用于摘要认证
void CvtHex( IN HASH Bin, OUT HASHHEX Hex);
void DigestCalcHA1( IN INT8 * pszAlg, IN INT8 * pszUserName, IN INT8 * pszRealm,
	IN INT8 * pszPassword, IN INT8 * pszNonce,
	IN INT8 * pszCNonce, OUT HASHHEX SessionKey);
void DigestCalcResponse(IN HASHHEX HA1, IN INT8 * pszNonce, 
	IN INT8 * pszNonceCount, IN INT8 * pszCNonce,
	IN INT8 * pszQop, IN INT8 * pszMethod,
	IN INT8 * pszDigestUri, IN HASHHEX HEntity,
	OUT HASHHEX Response);
//字符串处理,去掉引号
void str_dequote(char *s);