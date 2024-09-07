'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useResultStore } from '@/store/resultStore'

export function AppPage() {
  const [file, setFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const router = useRouter()
  const setResult = useResultStore((state) => state.setResult)
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (file) {
      setIsUploading(true)
      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await fetch('http://192.170.2.36:5000/api/upload', {
          method:  'POST',
          body: formData,
        })

        if (response.ok) {
          const result = await response.json()
          console.log('File uploaded successfully:', result)
          setResult(result)
          console.log('Result after setting:', useResultStore.getState().result)
          router.push('/results')
        } else {
          // router.push('/results')
          throw new Error('File upload failed')
        }
      } catch (error) {
        console.error('Error uploading file:', error)
        // 여기에 에러 처리 로직을 추가할 수 있습니다 (예: 사용자에게 에러 메시지 표시)
        // router.push('/results')
      } finally {
        setIsUploading(false)
      }
    }
  }

  return (
    <div className="container mx-auto mt-10">
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle>카카오톡 채팅 기록 분석</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
            <p className="text-sm text-gray-500 mb-2">허용된 파일 형식: .txt, .csv</p>
              <Input type="file" onChange={handleFileChange} accept=".txt,.csv" />
            </div>
            <Button type="submit" disabled={!file || isUploading}>
              {isUploading ? '업로드 중...' : '분석 시작'}
            </Button>
          </form>
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-2">카카오톡 대화 내용 추출 방법</h3>
            <ol className="list-decimal list-inside space-y-2">
              <li>대화 내용 추출하고자 하는 채팅방 진입</li>
              <li>☰버튼 클릭 후 채팅방 설정 클릭</li>
              <li>대화 내용 관리 탭 클릭</li>
              <li>대화 내용 저장 버튼 클릭</li>
            </ol>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
