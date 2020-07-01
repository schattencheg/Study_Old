using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;
using STMWPF;
using System;

namespace STMWPF
{
    [TestClass]
    public class DocumentWriterTests
    {
        private MockRepository mockRepository;



        [TestInitialize]
        public void TestInitialize()
        {
            this.mockRepository = new MockRepository(MockBehavior.Strict);


        }

        [TestCleanup]
        public void TestCleanup()
        {
            this.mockRepository.VerifyAll();
        }

        private DocumentWriter CreateDocumentWriter()
        {
            return new DocumentWriter();
        }

        [TestMethod]
        public void Write_StateUnderTest_ExpectedBehavior()
        {
            // Arrange
            var unitUnderTest = this.CreateDocumentWriter();
            SteamDiscount discount = TODO;

            // Act
            unitUnderTest.Write(
                discount);

            // Assert
            Assert.Fail();
        }

        [TestMethod]
        public void SaveToDisk_StateUnderTest_ExpectedBehavior()
        {
            // Arrange
            var unitUnderTest = this.CreateDocumentWriter();
            string path = TODO;

            // Act
            unitUnderTest.SaveToDisk(
                path);

            // Assert
            Assert.Fail();
        }
    }
}
